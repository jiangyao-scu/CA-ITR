import argparse
from tqdm import tqdm
import torch
from torch.utils.data import DataLoader

import os
import shutil
from dataset import CODDataset
from CECNet import get_model
from evaluation import evalrank

def to_device(data, device="cuda"):
    if isinstance(data, (tuple, list)):
        return [to_device(item, device) for item in data]
    elif isinstance(data, dict):
        return {name: to_device(item, device) for name, item in data.items()}
    elif isinstance(data, torch.Tensor):
        return data.to(device=device, non_blocking=True)
    else:
        raise TypeError(f"Unsupported type {type(data)}. Only support Tensor or tuple/list/dict containing Tensors.")

def parse_args():
    parser = argparse.ArgumentParser(description='Parse args for testing trained_weight.')

    # project settings
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument('--resume_path', default='./Path/To/CECNet.pth')
    parser.add_argument('--gpu', default='1')

    # data settings
    parser.add_argument("--data_root", type=str, default='/Path/To/Data/')
    parser.add_argument("--dataset", type=str, default='CamoIT')
    parser.add_argument('--num_workers', default=2, type=int)

    parser.add_argument('--Expert', default=False) 

    args = parser.parse_args()
    return args


def eval(model, val_dataloader, device, args):
    model.eval()
    img_global_embs = []
    cap_global_embs = []

    with torch.no_grad():
        for image, text, mask, seg_imgs in tqdm(val_dataloader, desc='Evaluating', leave=True):
            image = image.to(device)

            if args.Expert:
                batch_images = to_device(seg_imgs["data"], device=device)
                img_global_emb, cap_global_emb = model(image, text, seg_imgs=batch_images)
            else:
                mask = mask.to(device)
                img_global_emb, cap_global_emb = model(image, text, mask=mask)

            img_global_embs.append(img_global_emb.cpu())
            cap_global_embs.append(cap_global_emb.cpu())

        img_global_embs = torch.cat(img_global_embs, dim=0)
        cap_global_embs = torch.cat(cap_global_embs, dim=0)

        final_results_i2t, final_results_t2i, rt, rti = evalrank(img_global_embs, cap_global_embs, args.dataset, device)


if __name__ == "__main__":
    args = parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if args.Expert:
        args.batch_size = 4

    CECNet, pre_process_train, pre_process_val = get_model(args, device)
    CECNet.to(device)

    if args.resume_path != '':
        print('resume from {}'.format(args.resume_path))
        state_dict = torch.load(args.resume_path, map_location='cpu')
        CECNet.clip_model.load_state_dict(state_dict)

    val_dataset = CODDataset(os.path.join(args.data_root, args.dataset), 'test')

    val_loader = DataLoader(dataset=val_dataset,
                             batch_size=args.batch_size,
                             num_workers=args.num_workers,
                             pin_memory=True,
                             shuffle=False,
                             )

    print(len(val_dataset))

    eval(CECNet, val_loader, device, args)



