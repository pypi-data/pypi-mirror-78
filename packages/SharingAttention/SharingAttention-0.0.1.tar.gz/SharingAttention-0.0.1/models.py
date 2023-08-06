# Sharing attention in generative adversarial networks
# Author: Shanfeng Hu (shanfeng.hu1991@gmail.com)
# Date: 10-August-2020


import torch
import torch.nn as nn
from operators import Linear, Conv1x1, Conv3x3, Upsample, Downsample, ChannelAttention

#######################################################################################################################
# Generator for 32x32 images
class G32(nn.Module):
    def __init__(self, latent_dim, use_sn, attention_mode):
        super(G32, self).__init__()

        self.attention_mode = attention_mode

        self.ac = nn.LeakyReLU(0.2)
        self.up = Upsample(2)

        self.linear = Linear(latent_dim, 64*4*4, use_sn)

        self.conv4_1 = Conv3x3(64, 64, use_sn)
        self.conv4_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'G-only'}:
            self.conv4_attention = ChannelAttention(64, 32, False)

        self.conv8_1 = Conv3x3(64, 64, use_sn)
        self.conv8_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'G-only'}:
            self.conv8_attention = ChannelAttention(64, 32, False)

        self.conv16_1 = Conv3x3(64, 64, use_sn)
        self.conv16_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'G-only'}:
            self.conv16_attention = ChannelAttention(64, 32, False)

        self.conv32_1 = Conv3x3(64, 64, use_sn)
        self.conv32_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'G-only'}:
            self.conv32_attention = ChannelAttention(64, 32, False)

        self.conv_image = Conv1x1(64, 3, use_sn)

    def feature(self, x, d32):
        f4 = torch.reshape(self.ac(self.linear(x)), (-1, 64, 4, 4))
        f4 = self.ac(self.conv4_1(f4))
        f4 = self.ac(self.conv4_2(f4))
        if self.attention_mode in {'both', 'G-only'}:
            f4 = f4 * self.conv4_attention(f4)
        elif self.attention_mode == 'D-shared':
            f4 = f4 * d32.conv4_attention(f4).detach()

        f8 = self.up(f4)
        f8 = self.ac(self.conv8_1(f8))
        f8 = self.ac(self.conv8_2(f8))
        if self.attention_mode in {'both', 'G-only'}:
            f8 = f8 * self.conv8_attention(f8)
        elif self.attention_mode == 'D-shared':
            f8 = f8 * d32.conv8_attention(f8).detach()

        f16 = self.up(f8)
        f16 = self.ac(self.conv16_1(f16))
        f16 = self.ac(self.conv16_2(f16))
        if self.attention_mode in {'both', 'G-only'}:
            f16 = f16 * self.conv16_attention(f16)
        elif self.attention_mode == 'D-shared':
            f16 = f16 * d32.conv16_attention(f16).detach()

        f32 = self.up(f16)
        f32 = self.ac(self.conv32_1(f32))
        f32 = self.ac(self.conv32_2(f32))
        if self.attention_mode in {'both', 'G-only'}:
            f32 = f32 * self.conv32_attention(f32)
        elif self.attention_mode == 'D-shared':
            f32 = f32 * d32.conv32_attention(f32).detach()

        return f32

    def forward(self, x, d32):
        f32 = self.feature(x, d32)
        return torch.tanh(self.conv_image(f32))


# Discriminator for 32x32 images
class D32(nn.Module):
    def __init__(self, use_sn, attention_mode):
        super(D32, self).__init__()

        self.attention_mode = attention_mode

        self.ac = nn.LeakyReLU(0.2)
        self.down = Downsample(2)

        self.conv_feature = Conv1x1(3, 64, use_sn)

        self.conv32_1 = Conv3x3(64, 64, use_sn)
        self.conv32_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            self.conv32_attention = ChannelAttention(64, 32, False)

        self.conv16_1 = Conv3x3(64, 64, use_sn)
        self.conv16_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            self.conv16_attention = ChannelAttention(64, 32, False)

        self.conv8_1 = Conv3x3(64, 64, use_sn)
        self.conv8_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            self.conv8_attention = ChannelAttention(64, 32, False)

        self.conv4_1 = Conv3x3(64, 64, use_sn)
        self.conv4_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            self.conv4_attention = ChannelAttention(64, 32, False)

        self.linear = Linear(64 * 4 * 4, 1, use_sn)

    def feature(self, x):
        f32 = self.ac(self.conv32_1(x))
        f32 = self.ac(self.conv32_2(f32))
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            f32 = f32 * self.conv32_attention(f32)

        f16 = self.down(f32)
        f16 = self.ac(self.conv16_1(f16))
        f16 = self.ac(self.conv16_2(f16))
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            f16 = f16 * self.conv16_attention(f16)

        f8 = self.down(f16)
        f8 = self.ac(self.conv8_1(f8))
        f8 = self.ac(self.conv8_2(f8))
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            f8 = f8 * self.conv8_attention(f8)

        f4 = self.down(f8)
        f4 = self.ac(self.conv4_1(f4))
        f4 = self.ac(self.conv4_2(f4))
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            f4 = f4 * self.conv4_attention(f4)

        return f4

    def forward(self, x):
        f32 = self.ac(self.conv_feature(x))
        f4 = self.feature(f32)
        return torch.squeeze(torch.sigmoid(self.linear(torch.reshape(f4, (-1, 64*4*4)))), dim=1)


#######################################################################################################################
# Generator for 64x64 images
class G64(G32):
    def __init__(self, latent_dim, use_sn, attention_mode):
        super(G64, self).__init__(latent_dim, use_sn, attention_mode)

        self.conv64_1 = Conv3x3(64, 64, use_sn)
        self.conv64_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'G-only'}:
            self.conv64_attention = ChannelAttention(64, 32, False)

    def feature(self, x, d64):
        f32 = super(G64, self).feature(x, d64)

        f64 = self.up(f32)
        f64 = self.ac(self.conv64_1(f64))
        f64 = self.ac(self.conv64_2(f64))
        if self.attention_mode in {'both', 'G-only'}:
            f64 = f64 * self.conv64_attention(f64)
        elif self.attention_mode == 'D-shared':
            f64 = f64 * d64.conv64_attention(f64).detach()

        return f64

    def forward(self, x, d64):
        f64 = self.feature(x, d64)
        return torch.tanh(self.conv_image(f64))


# Discriminator for 64x64 images
class D64(D32):
    def __init__(self, use_sn, attention_mode):
        super(D64, self).__init__(use_sn, attention_mode)

        self.conv64_1 = Conv3x3(64, 64, use_sn)
        self.conv64_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            self.conv64_attention = ChannelAttention(64, 32, False)

    def feature(self, x):
        f64 = self.ac(self.conv64_1(x))
        f64 = self.ac(self.conv64_2(f64))
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            f64 = f64 * self.conv64_attention(f64)

        # reuse the layers created in the parent class
        f32 = self.down(f64)
        f4 = super(D64, self).feature(f32)

        return f4

    def forward(self, x):
        f64 = self.ac(self.conv_feature(x))
        f4 = self.feature(f64)
        return torch.squeeze(torch.sigmoid(self.linear(torch.reshape(f4, (-1, 64*4*4)))), dim=1)


#######################################################################################################################
# Generator for 128x128 images
class G128(G64):
    def __init__(self, latent_dim, use_sn, attention_mode):
        super(G128, self).__init__(latent_dim, use_sn, attention_mode)

        self.conv128_1 = Conv3x3(64, 64, use_sn)
        self.conv128_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'G-only'}:
            self.conv128_attention = ChannelAttention(64, 32, False)

    def feature(self, x, d128):
        f64 = super(G128, self).feature(x, d128)

        f128 = self.up(f64)
        f128 = self.ac(self.conv128_1(f128))
        f128 = self.ac(self.conv128_2(f128))
        if self.attention_mode in {'both', 'G-only'}:
            f128 = f128 * self.conv128_attention(f128)
        elif self.attention_mode == 'D-shared':
            f128 = f128 * d128.conv128_attention(f128).detach()

        return f128

    def forward(self, x, d128):
        f128 = self.feature(x, d128)
        return torch.tanh(self.conv_image(f128))


# Discriminator for 128x128 images
class D128(D64):
    def __init__(self, use_sn, attention_mode):
        super(D128, self).__init__(use_sn, attention_mode)

        self.conv128_1 = Conv3x3(64, 64, use_sn)
        self.conv128_2 = Conv3x3(64, 64, use_sn)
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            self.conv128_attention = ChannelAttention(64, 32, False)

    def feature(self, x):
        f128 = self.ac(self.conv128_1(x))
        f128 = self.ac(self.conv128_2(f128))
        if self.attention_mode in {'both', 'D-only', 'D-shared'}:
            f128 = f128 * self.conv128_attention(f128)

        # reuse the layers created in the parent class
        f64 = self.down(f128)
        f4 = super(D128, self).feature(f64)

        return f4

    def forward(self, x):
        f128 = self.ac(self.conv_feature(x))
        f4 = self.feature(f128)
        return torch.squeeze(torch.sigmoid(self.linear(torch.reshape(f4, (-1, 64*4*4)))), dim=1)
