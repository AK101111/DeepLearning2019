import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader, Subset
import os

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.model_ = models.resnet18()
        # Architecture

        # Load pre-trained model
        self.load_weights('weights.pth')

    def load_weights(self, pretrained_model_path, cuda=True):
        # Load pretrained model
        pretrained_model = torch.load(f=pretrained_model_path, map_location="cuda" if cuda else "cpu")

        # Load pre-trained weights in current model
        with torch.no_grad():
            self.model_.load_state_dict(pretrained_model, strict=True)

        # Debug loading
        print('Parameters found in pretrained model:')
        pretrained_layers = pretrained_model.keys()
        for l in pretrained_layers:
            print('\t' + l)
        print('')

        for name, module in self.model_.state_dict().items():
            if name in pretrained_layers:
                assert torch.equal(pretrained_model[name].cpu(), module.cpu())
                print('{} have been loaded correctly in current model.'.format(name))
            else:
                raise ValueError("state_dict() keys do not match")

    def forward(self, x):
        return self.model_(x)
