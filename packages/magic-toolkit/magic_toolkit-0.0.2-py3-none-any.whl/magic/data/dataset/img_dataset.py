""" load dataset stored with format kitti"""

import glob
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from .dataset import Dataset


class ImgDataset(Dataset):
    def __init__(self, dataset_path, transform):
        self.transform = transform
        if dataset_path:
            try:
                self.img_dir = glob.glob(os.path.join(dataset_path, "*image*"))[0]
                assert os.path.exists(self.img_dir)
                self.label_dir = glob.glob(os.path.join(dataset_path, "*label*"))[0]
                assert os.path.exists(self.label_dir)
                self.npz_dir = os.path.join(dataset_path, "npz")
                os.makedirs(self.npz_dir, exist_ok=True)  # do noting if exists
            except:
                raise RuntimeError("dataset_path error")
            self.img_paths = []
            # get all paths of image between directory
            img_suffix = ["*.jpg", "*.png"]
            for fmt in img_suffix:
                ret = glob.glob(os.path.join(self.img_dir, fmt))
                self.img_paths.extend(ret)

    def __getitem__(self, index):
        sample = self.get_sample(index)
        # preprocess, data argument
        if self.transform:
            sample = self.transform(sample)
            assert isinstance(sample, dict), "need type: dict"

        return sample

    def __len__(self):
        return len(self.img_paths)

    def get_sample(self, index):
        img_path = self.img_paths[index]
        img_name = os.path.basename(img_path).split(".")[0]
        npz_path = os.path.join(self.npz_dir, img_name + ".npz")
        # pre-load from npz
        if os.path.exists(npz_path):
            return np.load(npz_path)
        # get ground truth from txt
        txt_path = os.path.join(self.label_dir, img_name + ".txt")
        assert os.path.exists(txt_path), "label error: {} does not exist".format(txt_path)
        with open(txt_path) as f:
            lines = [l.strip().split() for l in f.readlines()]

        sample = dict()
        try:
            sample["image"] = cv2.imread(img_path)
            sample["label"] = np.array(lines)
        except Exception as err:
            print(err)

        np.savez(npz_path, **sample)
        return sample

    def split(self, test_size=0.3, shuffle=True):
        set1 = ImgDataset(None, None)
        set1.img_dir = self.img_dir
        set1.label_dir = self.label_dir
        set1.npz_dir = self.npz_dir
        set1.transform = self.transform

        set2 = ImgDataset(None, None)
        set2.img_dir = self.img_dir
        set2.label_dir = self.label_dir
        set2.npz_dir = self.npz_dir
        set2.transform = self.transform

        train_x, test_x = train_test_split(self.img_paths, test_size=test_size, random_state=100, shuffle=shuffle)
        set1.img_paths = train_x
        set2.img_paths = test_x
        return set1, set2
