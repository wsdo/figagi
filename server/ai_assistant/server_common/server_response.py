'''
Author: yuyingtao yuyingtao@agiclas.cn
Date: 2023-06-25 17:39:53
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-25 18:00:12
Description: 
'''
from typing import TypeVar, Generic

T = TypeVar('T')

class ServerResponse(Generic[T]):
    def __init__(self) -> None:
        self.is_success = True
        self.code = 0
        self.message = ''
        self.data: T = None