# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     fo
   Description :
   Author :        Asdil
   date：          2019/12/26
-------------------------------------------------
   Change Activity:
                   2019/12/26:
-------------------------------------------------
"""
__author__ = 'Asdil'
# 文件操作
import os
import shutil
from aftool import tool


def is_dir(path):
    """
    是否是文件夹
    :param path:  路径
    :return:
    """
    return os.path.isdir(path)


def is_file(path):
    """
    是否是文件夹
    :param path:  路径
    :return:
    """
    return os.path.isfile(path)


def is_exist(path):
    """
    是否存在该文件
    :param path:  路径
    :return:
    """
    return os.path.exists(path)


def del_file(path):
    """
    删除文件
    :param path:  路径
    :return:
    """
    flag = True
    try:
        os.remove(path)
    except BaseException:
        flag = False
    return flag


def del_dir(path):
    """
    删除文件夹
    :param path:  路径
    :return:
    """
    flag = True
    try:
        shutil.rmtree(path)
    except BaseException:
        flag = False
    return flag


def del_all_files(path, key=None):
    """
    删除目录下所有文件
    :param path:
    :param key:
    :return:
    """
    if key is None:
        files = tool.get_files(path)
    else:
        files = tool.get_files(path, key=key)
    for _file in files:
        if is_file(_file):
            del_file(_file)
        else:
            del_dir(_file)
    return True


def copy_all_files(srcfile, dstfile, key=None, isreplace=False):
    """
    拷贝目录下所有文件
    :param srcfile:
    :param dstfile:
    :param key:
    :param isreplace:
    :return:
    """
    if key is None:
        files = tool.get_files(srcfile)
    else:
        files = tool.get_files(srcfile, key=key)
    if isreplace:
        for _file in files:
            if is_file(_file):
                _, _, _, name = tool.split_path(_file)
                if is_exist(_file):
                    del_file(tool.path_join(dstfile, name))
                tool.copy_file(_file, dstfile)
            else:
                _, _, _, name = tool.split_path(_file)
                if is_exist(_file):
                    del_dir(tool.path_join(dstfile, name))
                shutil.copytree(_file, dstfile + f'/{name}')
    else:
        for _file in files:
            if is_file(_file):
                tool.copy_file(_file, dstfile)
            else:
                _, _, _, name = tool.split_path(_file)
                shutil.copytree(_file, dstfile + f'/{name}')


def cut_all_files(srcfile, dstfile, key=None, isreplace=False):
    """
    拷贝目录下所有文件
    :param srcfile:
    :param dstfile:
    :param key:
    :param isreplace:
    :return:
    """
    if key is None:
        files = tool.get_files(srcfile)
    else:
        files = tool.get_files(srcfile, key=key)
    if isreplace:
        for _file in files:
            if is_file(_file):
                _, _, _, name = tool.split_path(_file)
                if is_exist(_file):
                    del_file(tool.path_join(dstfile, name))
                tool.cut_file(_file, dstfile)
            else:
                _, _, _, name = tool.split_path(_file)
                if is_exist(_file):
                    del_dir(tool.path_join(dstfile, name))
                shutil.move(_file, dstfile + f'/{name}')
                print(f'copy {_file} -> dstfile/{name}')
    else:
        for _file in files:
            if is_file(_file):
                tool.cutFile(_file, dstfile)
            else:
                _, _, _, name = tool.splitPath(_file)
                shutil.move(_file, dstfile + f'/{name}')
                print(f'copy {_file} -> dstfile/{name}')


def cut_all_files(srcfile, dstfile, key=None, isreplace=False):
    """
    拷贝目录下所有文件
    :param srcfile:
    :param dstfile:
    :param key:
    :param isreplace:
    :return:
    """
    if key is None:
        files = tool.get_files(srcfile)
    else:
        files = tool.get_files(srcfile, key=key)
    if isreplace:
        for _file in files:
            if is_file(_file):
                _, _, _, name = tool.split_path(_file)
                if is_exist(_file):
                    del_file(tool.path_join(dstfile, name))
                tool.cut_file(_file, dstfile)
            else:
                _, _, _, name = tool.split_path(_file)
                if is_exist(_file):
                    del_dir(tool.path_join(dstfile, name))
                shutil.move(_file, dstfile + f'/{name}')
                print(f'cut {_file} -> dstfile/{name}')
    else:
        for _file in files:
            if is_file(_file):
                tool.cut_file(_file, dstfile)
            else:
                _, _, _, name = tool.split_path(_file)
                shutil.move(_file, dstfile + f'/{name}')
                print(f'cut {_file} -> dstfile/{name}')
