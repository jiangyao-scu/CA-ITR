import os
import pandas as pd
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset
import torch
import json
import cv2
import numpy as np
import torch.nn.functional as F


class CODDataset(Dataset):
    def __init__(self, data_root, mode='train', image_transform=None):

        self.image_root_dir = os.path.join(data_root, 'images')
        self.mask_root_dir = os.path.join(data_root, 'mask_zoomnext')
        self.json_file = os.path.join(data_root, '{}.json'.format(mode))
        self.data = []
        self.image_transform = image_transform

        with open(self.json_file, 'r') as f:
            json_data = json.load(f)

            for item in json_data:
                image_path = os.path.join(self.image_root_dir, item["name"])
                mask_path = os.path.join(self.mask_root_dir, item["name"].replace('.jpg', '.png'))
                text = item["caption3"]

                self.data.append((image_path, text, mask_path))

        if image_transform is None:
            self.image_transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.48145466, 0.4578275, 0.40821073), std=(0.26862954, 0.26130258, 0.27577711))
            ])

        self.mask_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image_path, text, mask_path = self.data[idx]

        img = self.image_transform(Image.open(image_path).convert('RGB'))
        mask = self.mask_transform(Image.open(mask_path).convert('L'))

        seg_imgs = load_ims_for_expert(image_path)

        return img, text, mask, seg_imgs


def resize(image_array: np.ndarray, height, width, interpolation=cv2.INTER_LINEAR):
    h, w = image_array.shape[:2]
    if h == height and w == width:
        return image_array

    resized_image_array = cv2.resize(image_array, dsize=(width, height), interpolation=interpolation)
    return resized_image_array


def load_ims_for_expert(path):
    bgr_array = cv2.imread(path, cv2.IMREAD_COLOR)
    rgb_array = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2RGB)
    images = [resize(rgb_array, height=int(384 * s), width=int(384 * s), interpolation=cv2.INTER_LINEAR) for s in (0.5, 1.0, 1.5)]
    image_s = torch.from_numpy(images[0]).div(255).permute(2, 0, 1)
    image_m = torch.from_numpy(images[1]).div(255).permute(2, 0, 1)
    image_l = torch.from_numpy(images[2]).div(255).permute(2, 0, 1)
    seg_img = dict(
        data={"image_s": image_s, "image_m": image_m, "image_l": image_l},
        info=dict(mask_path=path, group_name="image"),
    )
    return seg_img
