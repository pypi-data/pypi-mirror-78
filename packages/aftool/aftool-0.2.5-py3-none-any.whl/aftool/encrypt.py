# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     encryption
   Description :
   Author :       艾登科技 Asdil
   date：          2020/7/10
-------------------------------------------------
   Change Activity:
                   2020/7/10:
-------------------------------------------------
"""
__author__ = 'Asdil'
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


def base_encrypt(data):
    """base_encrypt方法用于base64转码

    Parameters
    ----------
    data : str
        需要转码的字符串
    Returns
    ----------
    """
    data = bytes(data, encoding="utf8")
    encrypt_data = base64.b64encode(data)
    encrypt_data = str(encrypt_data, encoding="utf8")
    return encrypt_data


def base_decrypt(data):
    """base_decrypt方法用于

    Parameters
    ----------
    data : str
        转码后字段

    Returns
    ----------
    """
    data = bytes(data, encoding="utf8")
    decrypt_data = base64.b64decode(data)
    decrypt_data = str(decrypt_data, encoding="utf8")
    return decrypt_data

