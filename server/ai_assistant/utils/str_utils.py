'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-26 00:55:29
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-26 00:56:55
Description: 
'''

# 截取字符串的后半段
def tract_prefix(full_str, prefix):
    if prefix in full_str:
        return full_str.split(prefix, 1)[1]
    else:
        return full_str
