'''
Author: yuyingtao yuyingtao@agiclas.cn
Date: 2023-06-18 00:15:59
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-24 01:01:51
Description: 
'''
from typing import Optional, List
from datetime import datetime
from ai_assistant.content_manager.content import (
    ContentTypeEnum,
    ContentCategoryEnum,
    FileTypeEnum)

class ContentEmbedding:
    def __init__(self):
        self.id: Optional[int] = None
        self.content_id: Optional[int] = None
        self.origin:  Optional[str] = None
        self.content_type = ContentTypeEnum.WebPage
        self.file_type: Optional[int] = FileTypeEnum.TXT
        self.content_category = ContentCategoryEnum.AI
        self.content_title: Optional[str] = None
        self.target_url: Optional[str] = None
        self.created = datetime.now(),
        self.updated = datetime.now(),
