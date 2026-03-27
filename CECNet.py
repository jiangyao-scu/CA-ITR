import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import os
import open_clip
from open_clip.transformer import LayerNorm
from methods import PvtV2B5_ZoomNeXt


class GraphAttention(nn.Module):
    def __init__(self, dim, rank=32, num_heads=8, qkv_bias=False, qk_scale=None, attn_drop=0., proj_drop=0., att=False):
        super().__init__()
        self.num_heads = num_heads
        head_dim = rank // (2*num_heads)

        self.scale = qk_scale or head_dim ** -0.5
        self.rank = rank
        self.q = nn.Linear(dim, self.rank, bias=qkv_bias)
        self.proj = nn.Linear(self.rank, self.rank)
        self.proj_drop = nn.Dropout(proj_drop)
        self.ln_1 = nn.Identity()
        self.ln_2 = LayerNorm(self.rank)
        self.mlp = nn.Linear(self.rank, dim)
        self.drop = nn.Dropout(attn_drop)

        self.reset_parameters()

    def reset_parameters(self) -> None:
        for name, param in self.named_parameters():
            nn.init.zeros_(param)

    def generate_attn_mask_fgandbg(self, q, k, cam_feature):
        q_B, q_N, q_C = q.shape # b, 1, c
        k_B, k_N, k_C = k.shape # b, l, c

        pooled_mask = F.max_pool2d(cam_feature, kernel_size=32, stride=32)
        pooled_mask = pooled_mask.squeeze(1).float()
        pooled_mask = pooled_mask.reshape(q_B, -1)

        mask_fg = torch.ones((q_B, q_N, k_N)).to(q.device)
        mask_bg = torch.ones((q_B, q_N, k_N)).to(q.device)

        mask_fg[:, :, 1:int(k_N/2)] = pooled_mask.unsqueeze(1)
        mask_fg[:, :, int(k_N/2)+1:k_N] = pooled_mask.unsqueeze(1)

        mask_bg[:, :, 1:int(k_N/2)] = (1-pooled_mask).unsqueeze(1)
        mask_bg[:, :, int(k_N/2):] = torch.zeros((q_B, 1, int(k_N/2))).to(q.device)

        return mask_fg, mask_bg

    def attention(self, q, k, cam_feature):
        q = self.q(q)
        k = self.q(k)

        q_fg = q[:, :, :64]
        q_bg = q[:, :, 64:]
        k_fg = k[:, :, :64]
        k_bg = k[:, :, 64:]
        v_fg = k_fg
        v_bg = k_bg

        q_B, q_N, q_C = q.shape
        mask_fg, mask_bg = self.generate_attn_mask_fgandbg(q, k, cam_feature)

        # fg
        attn_fg = (q_fg @ k_fg.transpose(-2, -1)) * (1 / math.sqrt(int(q_C/2)))
        attn_fg = attn_fg.softmax(dim=-1)
        attn_fg = attn_fg * mask_fg
        x_fg = (attn_fg @ v_fg).transpose(1, 2).reshape(q_B, q_N, int(q_C/2))
        # bg
        attn_bg = (q_bg @ k_bg.transpose(-2, -1)) * (1 / math.sqrt(int(q_C/2)))
        attn_bg = attn_bg.softmax(dim=-1)
        attn_bg = attn_bg * mask_bg
        x_bg = (attn_bg @ v_bg).transpose(1, 2).reshape(q_B, q_N, int(q_C / 2))

        x = torch.cat((x_fg, x_bg), dim=2)
        x = self.proj(x)
        x = self.proj_drop(x)

        return x

    def forward(self, q, k, cam_feature):
        shortcut = q
        x = self.attention(self.ln_1(q.clone()), self.ln_1(k.clone()), cam_feature)
        x = shortcut + self.drop(self.mlp(self.ln_2(x)))

        return x


class CCGA(nn.Module):
    def __init__(self):
        super().__init__()

        self.ADF = nn.Sequential(nn.Linear(3, 3, bias=False))
        self.Graph = GraphAttention(768, 128, 1)

    def reset_parameters(self) -> None:
        for name, param in self.named_parameters():
            if 'attention' in name:
                nn.init.zeros_(param)

    def forward(self, clip_feat: torch.Tensor, cam_feat: torch.Tensor, cam_feature: torch.tensor): # [b, 50, 768] # [b, 64, 96, 96]
        # print(clip_feat.shape)
        feat = torch.cat((clip_feat, cam_feat), dim=1)
        attention_output = self.Graph(clip_feat[:, 0, :].clone().unsqueeze(1), feat, cam_feature)
        fusion_input = torch.cat((clip_feat[:, 0, :].unsqueeze(1), attention_output, cam_feat[:, 0, :].unsqueeze(1)), dim=1)
        fusion_input = fusion_input.transpose(1, 2)
        fusion_output = torch.sum(torch.softmax(self.ADF(fusion_input), dim=-1) * fusion_input, dim=2)
        clip_feat[:, 0, :] = fusion_output

        return cam_feat, clip_feat


class CECNet(nn.Module):
    def __init__(self, expert_model, clip_model, tokenizer, device):
        super(CECNet, self).__init__()
        self.expert = expert_model
        self.clip_model = clip_model
        self.device = device
        self.tokenizer = tokenizer

        self.clip_model.visual.transformer.CCGAs_nums = 12
        self.clip_model.visual.transformer.CCGAs = nn.ModuleList()
        for i in range(self.clip_model.visual.transformer.CCGAs_nums):
            self.clip_model.visual.transformer.CCGAs.append(CCGA())

    def forward(self, image, text, mask=None, seg_imgs=None):
        if mask is not None:
            mask = mask
        elif seg_imgs is not None:
            with torch.no_grad():
                logits = self.expert(data=seg_imgs)
                probs = logits.sigmoid()
                probs = probs - probs.min()
                mask = probs / (probs.max() + 1e-8)
                mask = F.interpolate(mask, (224, 224))

        input_img = torch.cat((image, image * mask), dim=0)
        img_gobal_emb = self.clip_model.encode_image(input_img, cam_feature=mask, normalize=True, return_hidden=False)   # open_clip/model/CLIP

        text = self.tokenizer(text).to(self.device)
        cap_gobal_emb = self.clip_model.encode_text(text, normalize=True, return_hidden=False)

        return img_gobal_emb, cap_gobal_emb

    def save(self, path):
        torch.save(self.clip_model.state_dict(), os.path.join(path, 'CECNet.pth'))
        torch.save(self.clip_model.visual.transformer.CCGAs.state_dict(), os.path.join(path, 'CCGAs.pth'))


def get_model(args, device):
    if args.Expert:
        cam_model = PvtV2B5_ZoomNeXt(pretrained=False)
        cam_model.load_state_dict(torch.load('./pretrained/ZoomNeXt_retrain.pth', map_location='cpu'))
    else:
        cam_model = None

    clip, pre_process_train, pre_process_val = open_clip.create_model_and_transforms(model_name='ViT-B-32', pretrained="./pretrained/ViT-B-32.pt")
    tokenizer = open_clip.get_tokenizer('ViT-B-32')

    model = CECNet(cam_model, clip, tokenizer, device)

    return model, pre_process_train, pre_process_val
