# Sharing attention in generative adversarial networks
# Author: Shanfeng Hu (shanfeng.hu1991@gmail.com)
# Date: 10-August-2020


from math import sqrt
import pprint
import time
import torch
import numpy as np
import torch.nn.functional as F
from datetime import datetime
from torchvision import datasets
from torch.utils.data import DataLoader, ConcatDataset, Subset, random_split
import torchvision.transforms as transforms
from torchvision.utils import make_grid
from tensorboardX import SummaryWriter
import models
import utils
import pyinputplus as pyip
from torchsummary import summary


fmt = '{0:=^100}'
print(fmt.format('Specify hyper parameters (press ENTER to use defaults)'))
params = {
    'task': pyip.inputChoice(choices=['CIFAR10', 'CelebA'], blank=True) or 'CIFAR10',
    'max_samples': pyip.inputInt(prompt='Maximum number of samples (default=50000):\n', greaterThan=0, blank=True) or 50000,
    'test_size': pyip.inputFloat(prompt='Fraction of samples for testing (default=0.2):\n', greaterThan=0, lessThan=1, blank=True) or 0.2,
    'seed': pyip.inputInt(prompt='Random seed (default=0):\n', blank=True) or 0,
    'latent_dim': pyip.inputInt(prompt='Dimension of input noise (default=128):\n', greaterThan=0, blank=True) or 128,
    'attention_mode': pyip.inputChoice(choices=['none', 'both', 'G-only', 'D-only', 'D-shared'], blank=True) or 'none',
    'use_sn': pyip.inputBool(prompt='Whether to use spectral normalization (default=True):\n', blank=True) or True,
    'epochs': pyip.inputInt(prompt='Number of training epochs (default=1000):\n', greaterThan=0, blank=True) or 1000,
    'batch_size': pyip.inputInt(prompt='Mini-batch size (default=64):\n', greaterThan=0, blank=True) or 64,
    'G_lr': pyip.inputFloat(prompt='LR for generator (default=1e-4):\n', greaterThan=0, lessThan=1e-3, blank=True) or 1e-4,
    'D_lr': pyip.inputFloat(prompt='LR for discriminator (default=1e-4):\n', greaterThan=0, lessThan=1e-3, blank=True) or 1e-4,
    'device': torch.device(pyip.inputChoice(choices=['cpu'] if not torch.cuda.is_available() else (
            ['cpu'] + ['cuda:'+str(i) for i in range(torch.cuda.device_count())]), blank=True) or 'cpu'),
}

pprint.pprint(params, indent=4)
if not (pyip.inputBool('Are the above parameter settings correct (default=True):\n', blank=True) or True):
    print('Exiting training')
    exit(0)

print(fmt.format('Setup random seed'))
utils.set_random_seed(params['seed'])


print(fmt.format('Setup experiment log'))
exp_name = ','.join([str(v) for v in params.values()]) + ',' + datetime.now().strftime("%Y-%m-%d %H-%M-%S")
print(exp_name)
logger = SummaryWriter(log_dir='runs/'+exp_name)


print(fmt.format('Load training images'))
if params['task'] == 'CIFAR10':
    # 32x32 images
    image_size = 32
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )
    dataset = ConcatDataset((
        datasets.CIFAR10('data', train=True, download=True, transform=transform),
        datasets.CIFAR10('data', train=False, download=True, transform=transform)
    ))
elif params['task'] == 'CelebA':
    # 128x128 images
    image_size = 128
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )
    dataset = datasets.ImageFolder('data/celeba', transform=transform)
else:
    image_size, dataset = None, None

if len(dataset) > params['max_samples']:
    dataset = Subset(dataset, np.random.choice(len(dataset), size=params['max_samples'], replace=False))
test_size = int(len(dataset)*params['test_size'])
train_set, test_set = random_split(dataset, [len(dataset)-test_size, test_size],
                                   generator=torch.Generator().manual_seed(params['seed']))
print('Number of images:', len(train_set), 'for training', len(test_set), 'for testing')
print('Image size:', image_size)


print(fmt.format('Build networks'))
if image_size == 32:
    G = models.G32(params['latent_dim'], params['use_sn'], params['attention_mode']).to(params['device'])
    D = models.D32(params['use_sn'], params['attention_mode']).to(params['device'])
elif image_size == 64:
    G = models.G64(params['latent_dim'], params['use_sn'], params['attention_mode']).to(params['device'])
    D = models.D64(params['use_sn'], params['attention_mode']).to(params['device'])
elif image_size == 128:
    G = models.G128(params['latent_dim'], params['use_sn'], params['attention_mode']).to(params['device'])
    D = models.D128(params['use_sn'], params['attention_mode']).to(params['device'])
else:
    G, D = None, None

print('Summary of discriminator:')
summary(D, (params['batch_size'], 3, image_size, image_size), batch_dim=None, device=params['device'], depth=1)

print('Summary of generator:')
summary(G, (params['batch_size'], params['latent_dim']), D, batch_dim=None, device=params['device'], depth=1)

print(fmt.format('Create optimizers'))
G_optimizer = torch.optim.Adam(G.parameters(), lr=params['G_lr'])
D_optimizer = torch.optim.Adam(D.parameters(), lr=params['D_lr'])


print(fmt.format('Start training'))
global_step = 0
train_loader = DataLoader(train_set, shuffle=True, drop_last=True, batch_size=params['batch_size'])
fixed_noise = torch.randn((params['batch_size'], params['latent_dim']), device=params['device'], dtype=torch.float32)
for epoch in range(1, params['epochs']+1):
    start_time = time.time()

    # turn on the training flags
    D.train()
    G.train()

    # for each batch of real samples
    for _, (real_samples, _) in enumerate(train_loader):
        real_samples = real_samples.to(params['device'])

        # sample random noise
        noise = torch.randn((params['batch_size'], params['latent_dim']), device=params['device'], dtype=torch.float32)

        # generate fake samples from the noise
        fake_samples = G(noise, D)

        # update the discriminator
        fake_targets = torch.tensor([0.0]*params['batch_size'], device=params['device'], dtype=torch.float32)
        real_targets = torch.tensor([1.0]*params['batch_size'], device=params['device'], dtype=torch.float32)
        fake_loss = F.binary_cross_entropy(D(fake_samples.detach()), fake_targets)
        real_loss = F.binary_cross_entropy(D(real_samples), real_targets)
        D_loss = (fake_loss + real_loss)
        D_optimizer.zero_grad()
        D_loss.backward()
        D_optimizer.step()

        # update the generator
        G_loss = F.binary_cross_entropy(D(fake_samples), real_targets)
        G_optimizer.zero_grad()
        G_loss.backward()
        G_optimizer.step()

        # output
        global_step += 1
        logger.add_scalar('Loss/D_loss', D_loss.cpu().item(), global_step)
        logger.add_scalar('Loss/G_loss', G_loss.cpu().item(), global_step)

    # show the generated samples
    D.eval()
    G.eval()
    fake_samples = G(fixed_noise, D)
    logger.add_image('Sample/fake_samples', make_grid(fake_samples.cpu(), nrow=int(sqrt(params['batch_size'])),
                                                      normalize=True), global_step)

    # save a checkpoint
    torch.save(D.state_dict(), 'runs/' + exp_name + '/D-' + str(epoch) + '.model')
    torch.save(G.state_dict(), 'runs/'+exp_name+'/G-'+str(epoch)+'.model')

    print('Epoch', str(epoch)+'/'+str(params['epochs']), 'using', '{:0.3f}'.format(time.time()-start_time), 'seconds')
