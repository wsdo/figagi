'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-14 09:47:01
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-07-01 00:54:28
Description: 
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
from .spiders.wx_article import WxArticleSpider
import requests

api_base_url = "http://ta.agiclass.ai/admin"
# api_base_url = "http://localhost:7776"


class WxSpiderPipeline:
    def process_item(self, item, spider):
        return item

class SaveContentPipline:
    def process_item(self, item, spider):
        SERVER_TOKEN = os.getenv("SERVER_TOKEN", None)
        print(f'SaveContentPipline: {SERVER_TOKEN}')
        if (not isinstance(spider, WxArticleSpider)) or (SERVER_TOKEN is None):
            return item

        ret = requests.post(f'{api_base_url}/api/a/check_create_content', json={
            "title": item.get('title'),
            "type": "webpage",
            "file_type": "none",
            "origin": item.get('link'),
            "target_url": item.get('link'),
            "big_text": item.get('text'),
            "category": "ai",
            "note": item.get('note'),
            "token":  SERVER_TOKEN
        })

        print(f'save content pipline save result: {ret.content}')
        return item