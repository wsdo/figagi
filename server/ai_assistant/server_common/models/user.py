'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-25 22:58:28
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-25 22:58:56
Description: 
'''
from pydantic import BaseModel

class UserModel(BaseModel):
    username: str