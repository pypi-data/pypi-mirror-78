# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     geno
   Description :
   Author :        Asdil
   date：          2020/2/6
-------------------------------------------------
   Change Activity:
                   2020/2/6:
-------------------------------------------------
"""
__author__ = 'Asdil'
import pandas as pd
import numpy as np
import gzip


# 识别过滤的行数
def skipRow(path, key):
    skip = 0
    with open(path, 'r') as f:
        for line in f:
            if key == line[:len(key)]:
                return skip
            skip += 1
    return skip


# 读取call文件
def readCall(path, key='probeset_id'):
    df = pd.read_table(path, skiprows=skipRow(path, key), low_memory=False)
    return df


# 读取vcf
def readVcf(path, key='#CHROM'):
    df = pd.read_table(path, skiprows=skipRow(path, key), low_memory=False)
    return df


def skipRowGZ(path):
    skiprows = 0
    with gzip.open(path, 'rb') as f:
        for line in f:
            line = line.decode('utf-8')
            if line[0] != '#':
                break
            skiprows += 1
    skiprows -= 1
    return skiprows


# 读取vcf
def readVcfGZ(path):
    df = pd.read_table(path, skiprows=skipRowGZ(path), low_memory=False)
    return df


# 计算厘摩
class geneticMap(object):
    """keeps track of genetic Map locations and returns closest genetic map
    location given a snp location. """

    def __init__(self, file):
        """Builds conversion object for mapping base-pair position to genetic map position.
        Parameters:
        - `file` - tab delimited file with three columns: position [bp], combined rate [cM/Mb], Genetic Map [cM].
                   Example files for human genome release 36 can be found at:
                      ftp://ftp.hapmap.org/hapmap/recombination/2008-03_rel22_B36/rates/
                   and for relase 37 at:
                      ftp://ftp.hapmap.org/hapmap/recombination/2011-01_phaseII_B37/genetic_map_HapMapII_GRCh37.tar.gz
        """
        fp = open(file)
        # re-code the column name
        self.m = np.asarray([np.asarray(l.split())[[1, 3]]
                             for l in fp.readlines()[1:]], np.float)

    def pos2gm(self, pos):
        """Converts position in bp to position in centiMorgans"""
        m = self.m
        pos = np.asarray(pos)
        results = np.empty(pos.shape, dtype=np.float)
        # 查询pos元素在m[:,0]这个序列中得位置
        # Find probable locations in map 查询位点的遗传位置
        i = m[:, 0].searchsorted(pos)
        # Correct those that are beyond the end of the genetic map
        i[i == len(m)] = len(m) - 1
        # Fill results with those that match exactly
        idx = (m[i, 0] == pos) | (i == len(m) - 1) | (i == 0)
        results[idx] = m[i[idx], 1]

        idx = np.logical_not(idx)
        # Fill those that require interpolation
        results[idx] = (m[i[idx], 1] - m[i[idx] - 1, 1]) / (m[i[idx], 0] - m[i[idx] - 1, 0]) * \
                       (pos[idx] - m[i[idx] - 1, 0]) + m[i[idx] - 1, 1]
        return results


def hp():
    print(
        '计算厘摩: model = geneticMap("分染色体genomap文件")   pos=[1, 100] model.pos2gm(pos)')
