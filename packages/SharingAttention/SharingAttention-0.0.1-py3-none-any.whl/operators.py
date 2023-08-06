# Sharing attention in generative adversarial networks
# Author: Shanfeng Hu (shanfeng.hu1991@gmail.com)
# Date: 28-August-2020


import torch
import torch.nn as nn
from torch.nn.utils import spectral_norm


# Linear Operator
class Linear(nn.Module):
    def __init__(self, in_features, out_features, use_sn):
        super(Linear, self).__init__()

        self.linear = nn.Linear(in_features, out_features)

        if use_sn:
            # apply spectral normalization
            self.linear = spectral_norm(self.linear)

    def forward(self, x):
        return self.linear(x)


# Convolution 1x1 Operator
class Conv1x1(nn.Module):
    def __init__(self, in_channels, out_channels, use_sn):
        super(Conv1x1, self).__init__()

        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=(1, 1))

        if use_sn:
            # apply spectral normalization
            self.conv = spectral_norm(self.conv)

    def forward(self, x):
        return self.conv(x)


# Convolution 3x3 Operator
class Conv3x3(nn.Module):
    def __init__(self, in_channels, out_channels, use_sn):
        super(Conv3x3, self).__init__()

        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=(3, 3), padding=(1, 1))

        if use_sn:
            # apply spectral normalization
            self.conv = spectral_norm(self.conv)

    def forward(self, x):
        return self.conv(x)


# Upsampling Operator
class Upsample(nn.Module):
    def __init__(self, up_factor):
        super(Upsample, self).__init__()

        self.up = nn.Upsample(scale_factor=up_factor, mode='nearest')

    def forward(self, x):
        return self.up(x)


# Downsampling Operator
class Downsample(nn.Module):
    def __init__(self, down_factor):
        super(Downsample, self).__init__()

        self.down = nn.AvgPool2d(kernel_size=(down_factor, down_factor), stride=down_factor)

    def forward(self, x):
        return self.down(x)


# Channel Attention Operator
class ChannelAttention(nn.Module):
    def __init__(self, in_channels, bottleneck_dim, use_sn):
        super(ChannelAttention, self).__init__()

        self.ac = nn.Tanh()

        self.linear1 = Linear(in_channels, bottleneck_dim, use_sn)
        nn.init.zeros_(self.linear1.linear.weight)
        nn.init.zeros_(self.linear1.linear.bias)

        self.linear2 = Linear(bottleneck_dim, bottleneck_dim, use_sn)
        nn.init.zeros_(self.linear2.linear.weight)
        nn.init.zeros_(self.linear2.linear.bias)

        self.linear3 = Linear(bottleneck_dim, in_channels, use_sn)
        nn.init.zeros_(self.linear3.linear.weight)
        nn.init.zeros_(self.linear3.linear.bias)

    def forward(self, x):
        channel_features = torch.mean(x, dim=(2, 3))
        channel_features = self.ac(self.linear1(channel_features))
        channel_features = self.ac(self.linear2(channel_features))
        channel_weights = torch.sigmoid(self.linear3(channel_features))
        return torch.unsqueeze(torch.unsqueeze(channel_weights, dim=2), dim=3)


# Spatial Attention Operator
class SpatialAttention(nn.Module):
    def __init__(self, in_channels, bottleneck_dim, use_sn):
        super(SpatialAttention, self).__init__()

        self.ac = nn.Tanh()

        self.conv1 = Conv1x1(in_channels, bottleneck_dim, use_sn)
        nn.init.zeros_(self.conv1.conv.weight)
        nn.init.zeros_(self.conv1.conv.bias)

        self.conv2 = Conv1x1(bottleneck_dim, bottleneck_dim, use_sn)
        nn.init.zeros_(self.conv2.conv.weight)
        nn.init.zeros_(self.conv2.conv.bias)

        self.conv3 = Conv1x1(bottleneck_dim, 1, use_sn)
        nn.init.zeros_(self.conv3.conv.weight)
        nn.init.zeros_(self.conv3.conv.bias)

    def forward(self, x):
        spatial_features = self.ac(self.conv1(x))
        spatial_features = self.ac(self.conv2(spatial_features))
        spatial_weights = torch.sigmoid(self.conv3(spatial_features))
        return spatial_weights
