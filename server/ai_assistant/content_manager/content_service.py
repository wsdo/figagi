'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-17 18:48:10
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-28 20:46:15
Description: 
'''
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Optional, Literal, Tuple
from datetime import datetime
from ai_assistant.content_manager.content import Content



class ContentService(metaclass=ABCMeta):
    @abstractmethod
    def get_by_id(self, id: str) -> Content:
        pass

    @abstractmethod
    def search_contents(self, last_created: datetime, size: int = 10, must: List[Dict] = [], filter: List[Dict] = [], sort_order: Literal["desc", 'asc'] = 'desc') -> List[Content]:
        pass

    @abstractmethod
    def search_contents_paged(self, last_id: str, size: int = 10, must: List[Dict] = [], filter: List[Dict] = [], sort_order: Literal["desc", 'asc'] = 'desc') -> List[Content]:
        pass

    @abstractmethod
    def get_content_by_origin(self, origin: str) -> Optional[Content]:
        pass

    @abstractmethod
    def create(self, content: Content, text: str) -> Content:
        pass

    @abstractmethod
    def checkAndCreate(self, content: Content, text: str) -> Tuple[bool, Content]:
        pass

    @abstractmethod
    def update(self, content: Content):
        pass

    @abstractmethod
    def delete(self, id: str, logic = True):
        pass

    @abstractmethod
    def get_text(self, content: Content):
        pass