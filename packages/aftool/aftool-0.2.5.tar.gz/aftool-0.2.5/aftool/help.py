# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     help
   Description :
   Author :        艾登科技 Asdil
   date：          2020/8/31
-------------------------------------------------
   Change Activity:
                   2020/8/31:
-------------------------------------------------
"""
__author__ = 'Asdil'


def help_argparse():
    """help_argparse方法用于参数示例

    Parameters
    ----------
    param : str
        
    Returns
    ----------
    """
    print("import argparse")
    print("if __name__ == '__main__':")
    print("    args_parser = argparse.ArgumentParser(description='参数配置')")
    print("    args_parser.add_argument('--p', type=int, default=10, help='参数')")
    print("    args = args_parser.parse_args()")


def help_parallel():
    """help_parallel方法用于并行计算示例

    Parameters
    ----------
    param : str

    Returns
    ----------
    """
    print('from aftool import jobs')
    print('')
    print('def func():')
    print('    return 0')
    print('')
    print('args = []')
    print('mmp_df = jobs.memmap(mmp_df)')
    print('ret = jobs.parallel(args, func, njobs=8, backend=1)')


def help_ray():
    """ray方法用于ray是示例

    Parameters
    ----------
    param : str

    Returns
    ----------
    """
    print('import ray')
    print('ray.init(num_cpus=8)')
    print('args = []')
    print('')
    print('@ray.remote')
    print('def func(args):')
    print('    return 0')
    print('')
    print('df_id = ray.put(df) # 共享内存')
    print('ret = [f.remote() for i in args]')


def help_log():
    """help_log方法用于

    Parameters
    ----------
    param : str

    Returns
    ----------
    """

    print("logger = simple_init(level='INFO', log_path=None)")
    print("logger.info('第一种方法')")

    print("logger = init(log_path, level='INFO')")
    print("logger.info('第二种方法')")
    return 0


def help_pytorch():
    """help_pytorch方法用于显示简单的prtorch网络结构

    Parameters
    ----------
    param : str

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


def help_abspath():
    """help_path方法用于绝对路径

    Parameters
    ----------
    param : str

    Returns
    ----------
    """
    print("import os")
    print("abs_path = os.path.dirname(os.path.abspath(__file__))")
    print("father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))")


def help_fastapi():
    """help_fastapi方法用于fastapi示例

    Parameters
    ----------
    param : str

    Returns
    ----------
    """
    print("from fastapi import FastAPI")
    print("from pydantic import BaseModel")
    print("app = FastAPI()")
    print("class Args(BaseModel):")
    print("    data_str: str")
    print("    data_int: int")
    print("    data_list: list")
    print("")
    print("""@app.post("/test_post")""")
    print("async def postEchoApi(args:Args):")
    print("    dict_args = args.dict() # 也可以转化为字典")
    print("""    return {"str data":args.data_str,""")
    print("""    'int data': args.data_int,""")
    print("""    'list data':args.data_list,""")
    print("""    'args 数据类型': str(type(args))}""")
    print("")
    print("if __name__ == '__main__':")
    print("    import uvicorn")
    print("""    uvicorn.run(app, host="127.0.0.1", port=8000)""")
    return 0
