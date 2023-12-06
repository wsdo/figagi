'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-20 19:57:48
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-20 19:58:26
Description: 
'''
from typing import Optional
from datetime import datetime

class BigText:
    def __init__(self):
        self.id: Optional[str] = None
        self.text: Optional[str] = None
        self.deleted: int = 0
        self.created = datetime.now(),
        self.updated = datetime.now(),