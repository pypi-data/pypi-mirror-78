# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     deep
   Description :
   Author :        Asdil
   date：          2020/4/23
-------------------------------------------------
   Change Activity:
                   2020/4/23:
-------------------------------------------------
"""
__author__ = 'Asdil'


def example_pytorch():
    """get_simple_net方法用于显示简单的prtorch网络结构

    Parameters
    ----------

    Returns
    ----------
    """
    print('import torch')
    print('from torch import nn')
    print('from torch.nn import init')
    print('import torch.optim as optim')
    print('import torch.nn.functional as F')
    print('from torchvision import transforms')
    print('from torch.utils.data import Dataset')
    print('from torch.utils.data import DataLoader')
    print("device = torch.device('cuda' if torch.cuda.is_available else 'cpu')")
    print('')
    print('# 加载数据')
    print('class myDataset(Dataset):')
    print('    def __init__(self, feature, label, transform=None):')
    print('        self.feature = feature')
    print('        self.label = label')
    print('    def __len__(self):')
    print('        return len(self.feature)')
    print('    def __getitem__(self, idx):')
    print('        data = self.feature[idx,:]')
    print('        label = self.label[i]')
    print('        if self.transform:')
    print('            data = self.transform(data)')
    print('        return data, label')
    print('train_iter = DataLoader(dataset=, batch_size=, shuffle=True, num_workers=8)')
    print('')
    print('# 初始化权重')
    print('def _weight_init(m):')
    print('    if isinstance(m, nn.Linear):')
    print('        nn.init.xavier_uniform_(m.weight)')
    print('        nn.init.constant_(m.bias, 0)')
    print('    elif isinstance(m, nn.Conv2d):')
    print('        nn.init.xavier_uniform_(m.weight)')
    print('    elif isinstance(m, nn.BatchNorm1d):')
    print('        nn.init.constant_(m.weight, 1)')
    print('        nn.init.constant_(m.bias, 0)')
    print('')
    print('# 加载网络')
    print('class Net(nn.Module):')
    print('    def __init__(self):')
    print('        super(Net, self).__init__()')
    print('        self.apply(_weight_init) # 初始化权重')
    print('        do something...')
    print('    #正向传播 ')
    print('    def forward(self, x):')
    print('        do something...')
    print('        return x')
    print('')

    print('loss = nn.MSELoss()')
    print('optimizer = optim.SGD(net.parameters(), lr=0.03)')
    print('for epoch in range(1,epochs + 1):')
    print('    for X, y in data_iter:')
    print('        output = net(X)')
    print('        l = loss(output, y.view(-1, 1))')
    print('        optimizer.zero_grad() # 梯度清零，等价于net.zero_grad()')
    print('        l.backward()')
    print('        optimizer.step()')
    print("""    print('epoch %d, loss: %f' % (epoch, l.item()))""")