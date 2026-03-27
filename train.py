import argparse
from tqdm import tqdm
import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F

import os
import shutil
from dataset import CODDataset
from CECNet import get_model
from evaluation import evalrank


def parse_args():
    parser = argparse.ArgumentParser(description='Parse args for training trained_weight.')

    # project settings
    parser.add_argument('--output_dir', default='./Path/To/Save/Reults/')
    parser.add_argument('--seed', default=1, type=int)
    parser.add_argument('--frozen_clip',  action='store_true', default=False)
    parser.add_argument('--clip_lr', type=float, default=1e-5)
    parser.add_argument('--ccga_lr', type=float, default=1e-5)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument('--resume_path', default='')
    parser.add_argument('--gpu', default='0')
    parser.add_argument('--Expert',  action='store_true', default=False)

    # data settings
    parser.add_argument("--data_root", type=str, default='/Path/To/Data/')
    parser.add_argument("--dataset", type=str, default='CamoIT')
    parser.add_argument('--num_workers', default=2, type=int)
    parser.add_argument("--epochs", type=int, default=10)

    args = parser.parse_args()
    return args

def train(args, model, device, train_dataloader, val_dataloader, optimizer):
    losses = []
    epoches = []
    best_i2t_r1 = 0
    best_t2i_r1 = 0

    with open(os.path.join(args.output_dir, 'record.txt'), 'a') as f:
        f.writelines(f"{args.output_dir}:\n")
    f.close()

    torch.autograd.set_detect_anomaly(True)

    for epoch in range(args.epochs):
        model.train()
        epoch_loss = 0

        for idx, (image, text, mask, _) in enumerate(train_dataloader):
            optimizer.zero_grad()
            image = image.to(device)
            mask = mask.to(device)

            img_global_emb, cap_global_emb = model(image, text, mask=mask)

            i2t_sim = 20 * (img_global_emb @ cap_global_emb.T)
            t2i_sim = i2t_sim.T

            target = torch.eye(img_global_emb.shape[0], device=device)
            loss = (-torch.mean(F.log_softmax(i2t_sim, dim=1) * target, dim=1).mean()
                        -torch.mean(F.log_softmax(t2i_sim, dim=1) * target, dim=1).mean())

            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

            if idx % (10) == 0 and idx != 0:
                print(f"Epoch {epoch + 1}, Loss: {loss.item():.5f}")

        epoch_loss /= len(train_dataloader)
        losses.append(epoch_loss)
        epoches.append(epoch)

        print(f"Epoch {epoch + 1} completed. Average Loss: {epoch_loss}")

        val_results = eval(model, val_dataloader, device, epoch, epoch_loss)

        if val_results['I2T'][0] >= best_i2t_r1 and val_results['T2I'][0] >= best_t2i_r1:
            best_i2t_r1 = max(val_results['I2T'][0], best_i2t_r1)
            best_t2i_r1 = max(val_results['T2I'][0], best_t2i_r1)

            model.save(args.output_dir)

    return losses, epoches

def eval(model, val_dataloader, device, epoch, epoch_loss):
    model.eval()
    for dataset in val_dataloader:
        img_global_embs = []
        cap_global_embs = []

        with torch.no_grad():
            for image, text, mask, _ in tqdm(dataset, desc='Evaluating', leave=True):
                image = image.to(device)
                mask = mask.to(device)

                img_global_emb, cap_global_emb = model(image, text, mask=mask)

                img_global_embs.append(img_global_emb.cpu())
                cap_global_embs.append(cap_global_emb.cpu())

            img_global_embs = torch.cat(img_global_embs, dim=0)
            cap_global_embs = torch.cat(cap_global_embs, dim=0)

            final_results_i2t, final_results_t2i, rt, rti = evalrank(img_global_embs, cap_global_embs, 'COD', device)

        with open(os.path.join(args.output_dir, 'record.txt'), 'a') as f:
            f.writelines(f"Epoch {epoch + 1} completed. Average Loss: {epoch_loss:.5f}\n")
            f.writelines("Image to text (R@1, R@5, R@10): %.1f %.1f %.1f\n" % final_results_i2t[:3])
            f.writelines("Text to image (R@1, R@5, R@10): %.1f %.1f %.1f\n" % final_results_t2i[:3])
        f.close()

    results = {
        'I2T': final_results_i2t,
        'T2I': final_results_t2i
    }

    return results


if __name__ == "__main__":
    args = parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    model, pre_process_train, pre_process_val = get_model(args, device)
    model.to(device)
    print(pre_process_train)

    if args.frozen_clip:
        print('training CCGAs')
        for name, param in model.named_parameters():
            if 'CCGAs' in name:
                param.requires_grad = True
            else:
                param.requires_grad = False
    else:
        print('training CECNet')
        for name, param in model.named_parameters():
            param.requires_grad = True
        print('resume from {}'.format(args.resume_path))
        state_dict = torch.load(args.resume_path, map_location='cpu')
        model.clip_model.visual.transformer.CCGAs.load_state_dict(state_dict)

    param_groups = [
        {'params': [param for name, param in model.named_parameters() if 'CCGAs' in name],
         'lr': args.ccga_lr, 'name': 'CCGAs'},
        {'params': [param for name, param in model.named_parameters() if 'CCGAs' not in name],
         'lr': args.clip_lr, 'name': 'clip'},
    ]
    optimizer = torch.optim.Adam(param_groups, weight_decay=0.0001)

    train_dataset = CODDataset(os.path.join(args.data_root, args.dataset), 'train')
    val_dataset = CODDataset(os.path.join(args.data_root, args.dataset), 'test')

    train_loader = DataLoader(dataset=train_dataset, batch_size=args.batch_size, num_workers=args.num_workers,
                              pin_memory=True, shuffle=True)

    val_loader = DataLoader(dataset=val_dataset, batch_size=args.batch_size, num_workers=args.num_workers,
                            pin_memory=True, shuffle=False)

    loss, epochs = train(args, model, device, train_loader, [val_loader], optimizer)

# python train.py  --output_dir './models/test/CCGA/' --frozen_clip --ccga_lr 1e-4
# python train.py  --output_dir './models/test/CECNet/' --ccga_lr 1e-5 --resume_path './models/test/CCGA/CCGAs.pth'