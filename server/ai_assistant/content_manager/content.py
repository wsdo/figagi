'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-17 18:49:20
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-28 00:48:48
Description: 
'''
from dataclasses import dataclass
from datetime import datetime
from ai_assistant.common.type_enum import TypeEnum

class ContentTypeEnum(TypeEnum):
    FILE = ('文件', 'file', 0)
    WebPage = ('网页', 'webpage', 1)
    
    def __init__(self, text: str, code: str, val: int):
        super().__init__(text, code ,val)

class FileTypeEnum(TypeEnum):
    NONE = ('none', 'none', 0)
    TXT = ('txt', 'txt', 1)
    PDF = ('pdf', 'pdf', 2)
    DOCX = ('docx', 'docx', 3)

    def __init__(self, text: str, code: str, val: int):
        super().__init__(text, code ,val)
        
class ContentCategoryEnum(TypeEnum):
    AI = ('AI', 'ai', 0)

    def __init__(self, text: str, code: str, val: int):
        super().__init__(text, code ,val)

@dataclass
class Content:
    def __init__(self) -> None:
        self.id: str | None = None
        self.type: str | None = None
        self.title: str | None = None
        self.file_type: str | None = None
        self.origin: str | None = None
        self.target_url: str | None = None
        self.text_id: str | None = None
        self.category: str | None = None
        self.deleted: int = 0
        self.created: datetime | None = None
        self.updated: datetime | None = None 
        self.has_vectored: bool = False
        self.note: str | None = '' 