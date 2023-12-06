'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-20 20:00:01
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-20 23:56:13
Description: 
'''
from ai_assistant.content_manager.big_text import BigText
from abc import ABCMeta, abstractmethod

class BigTextService(metaclass=ABCMeta):
    @abstractmethod
    def get_by_id(self, id: str) -> BigText:
        pass

    @abstractmethod
    def create(self, content: BigText) -> BigText:
        pass

    @abstractmethod
    def create_by_text(self, text: str) -> BigText:
        pass

    @abstractmethod
    def update(self, content: BigText):
        pass

    @abstractmethod
    def delete(self, id: str, logic = True):
        pass