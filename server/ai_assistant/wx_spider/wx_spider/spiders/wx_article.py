'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-14 09:47:01
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-07-03 15:21:32
Description: 
'''
from typing import List

import scrapy
import json
from bs4 import BeautifulSoup


class WxArticleSpider(scrapy.Spider):
    name = "wx_article"
    allowed_domains = ["mp.weixin.qq.com"]
    start_urls = ["https://mp.weixin.qq.com"]

    custom_settings = {
        "DOWNLOAD_DELAY": 0,
        "AUTOTHROTTLE_START_DELAY": 0.1
    }
    # Get url or json from command line
    def __init__(self, json='', url='', msg_list: List = None, *args, **kwargs):
        super(WxArticleSpider, self).__init__(*args, **kwargs)
        self.url = url
        self.jsonfile = json
        self.msg_list = msg_list

    def start_requests(self):
        if (self.msg_list is not None) and len(self.msg_list) > 0:
            for item in self.msg_list:
                url = item['link']
                yield scrapy.Request(url, self.parse)
        elif self.url != '':
            yield scrapy.Request(self.url, self.parse)
        elif self.jsonfile is not None:
            with open(self.jsonfile, 'r') as f:
                data = json.load(f)
                for item in data:
                    url = item['link']
                    yield scrapy.Request(url, self.parse, cb_kwargs={ "note": json.dumps(item) })

    def parse(self, response, note):
        html_content = response.css('div.rich_media_content').get()
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator='\n')
        item = {
            'title': response.xpath('//meta[@property="og:title"]/@content').get(),
            'link': response.xpath('//meta[@property="og:url"]/@content').get(),
            'text': text,
            'note': note,
        }
        yield item
