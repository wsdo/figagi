'''
Author: yuyingtao yuyingtao@agiclas.cn
Date: 2023-06-18 23:16:11
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-19 13:59:42
Description: 
'''
from enum import Enum

class TypeEnum(Enum):
    def __init__(self, text: str, code: str, val: int):
        self.text = text
        self.code = code
        self.val = val