'''
Author: yuyingtao yuyingtao@agiclas.cn
Date: 2023-06-28 00:25:33
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-29 19:25:51
Description: 
'''
from ai_assistant.config.config import Config
from ai_assistant.content_manager.content_service import ContentService
from ai_assistant.content_manager.content import Content, ContentTypeEnum, FileTypeEnum
from ai_assistant.crawler.wexin_crawler import crawl_wx_platform
from ai_assistant.app.LangChainService import LangChainService
from ai_assistant.utils.text_utils import cut_sent_long
from ai_assistant.content_manager.content import FileTypeEnum, ContentTypeEnum
from ai_assistant.utils.logger import create_logger

logger = create_logger('app_service')

VECTOR_MIN_LENGTH = 300

class AppService:
    def __init__(self, config: Config, content_service: ContentService, langchain_service: LangChainService):
        self.config = config
        self.content_service = content_service
        self.langchain_service = langchain_service

    def crawl_wx_platform(self, fake_id: str, token: str, cookie: str, begin = 0, category: str = '', vecotr = False):
        items = crawl_wx_platform(fake_id=fake_id, token=token, cookie=cookie, begin=begin)

        success = 0
        failed = 0
        duplicated = 0

        for item in items:
            c = Content()
            c.title = item.get('title')
            c.type = ContentTypeEnum.WebPage.code
            c.file_type = FileTypeEnum.NONE.code
            c.category = category
            c.origin = item.get('link')
            c.target_url = item.get('link')
            c.has_vectored = vecotr
            c.note = item.get('note')

            text = item.get('text')
            try:
                ret = self.content_service.checkAndCreate(c, text=text)
                if ret[0]:
                    success += 1
                    if vecotr:
                        contents = cut_sent_long(text, VECTOR_MIN_LENGTH)
                        self.langchain_service.add_file_embedding(c.title, contents, c.origin, FileTypeEnum.NONE.code,
                            content_id=ret[1].id, content_type=ContentTypeEnum.WebPage.code, content_category=category)
                else:
                    duplicated += 1
            except Exception as err:
                logger.error('create crawl item failed %s', item)
                logger.error(err)
                failed += 1

        return {
            "success": success,
            "failed": failed,
            "duplicated": duplicated
        }

    # 向量化字符串
    def vector_content(self, content: Content, text: str):
        contents = cut_sent_long(text, VECTOR_MIN_LENGTH)
        self.langchain_service.add_file_embedding(content.title, contents, content.origin, FileTypeEnum.NONE.code,
            content_id=content.id, content_type=ContentTypeEnum.WebPage.code, content_category=content.category)

        content.has_vectored = True
        self.content_service.update(content=content)