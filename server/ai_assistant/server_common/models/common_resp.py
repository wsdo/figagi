'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-26 17:08:14
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-26 17:34:36
Description: 
'''
from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T", bound=BaseModel)

class CommonResp(GenericModel, Generic[T]):
    success: bool
    code: str
    message: str
    data: T

def create_success_resp(data: T) -> CommonResp[T]:
    return {
        'success': True,
        'code': '0000',
        'message': 'ok',
        'data': data
    }
    