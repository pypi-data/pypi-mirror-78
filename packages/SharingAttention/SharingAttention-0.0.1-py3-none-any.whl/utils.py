# Sharing attention in generative adversarial networks
# Author: Shanfeng Hu (shanfeng.hu1991@gmail.com)
# Date: 10-August-2020


import random
import numpy as np
import torch


def set_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
