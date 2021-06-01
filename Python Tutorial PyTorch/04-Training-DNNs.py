import torch
import torchvision
import numpy as np
import cv2
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from torchvision.utils import make_grid
from torch.utils.data.dataloader import DataLoader
from torch.utils.data import random_split

dataset = MNIST(root="data/", download=True, transform=ToTensor())
img, label = dataset[0]

# check the data
"""
print(img.shape, label)
plt.imshow(img[0], cmap="gray")
plt.show()
"""

# split the data
val_size = 10000
train_size = len(dataset) - val_size
train_ds, val_ds = random_split(dataset, [train_size, val_size])

batch_size = 128
train_loader = DataLoader(dataset, batch_size, shuffle=True, num_workers=4, pin_memory=True)
val_loader = DataLoader(dataset, batch_size*2, num_workers=4, pin_memory=True)


