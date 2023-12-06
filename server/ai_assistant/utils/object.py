'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-05-04 12:40:12
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-26 15:52:06
Description: 
'''
'''
'''
from typing import Dict
class Object:
    pass

def copyDictToObj(dict: Dict, obj, skipNone = True):
    for key, value in dict.items():
        if ((not hasattr(obj, key)) or (skipNone and not value)):
            continue
        setattr(obj, key, value)

def copyObjToObj(src: object, dst, skipNone = True):
    copyDictToObj(src.__dict__, dst, skipNone=skipNone) 