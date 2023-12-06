'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-14 09:47:01
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-07-02 23:52:56
Description: 
'''
import scrapy
import json
from dotenv import load_dotenv
import os

class WxArticleListSpider(scrapy.Spider):
    name = "wx_article_list"
    allowed_domains = ["mp.weixin.qq.com"]
    base_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin={begin}&count=5&fakeid={fakeid}&type=9&query=&token={token}&lang=zh_CN&f=json&ajax=1'

    def __init__(self, token="", fake_id="", cookie="", begin=0):
        self.token = token
        self.fake_id = fake_id
        self.cookie = cookie
        self.begin = begin


    # Get the json from the url
    def start_requests(self):
        if (not os.getenv('ENV_ENV')):
            load_dotenv()
        cookie = os.getenv("COOKIE", self.cookie)
        fakeid = os.getenv("FAKEID", self.fake_id)
        token = os.getenv("TOKEN", self.token)
        begin = int(os.getenv("BEGIN", self.begin)) 

        self.base_url = self.base_url.format(
            begin="{begin}", fakeid=fakeid, token=token)
        self.cookies = parse_cookie(cookie)

        self.begin = begin
        url = self.base_url.format(begin=self.begin)
        yield scrapy.Request(url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        if not data.get('app_msg_list'):
            return
        for item in data.get('app_msg_list'):
            yield item

        self.begin += 5
        url = self.base_url.format(begin=self.begin)
        print(f'crawler list url: {url}')
        yield scrapy.Request(url, cookies=self.cookies, callback=self.parse)


def parse_cookie(cookie_str):
    cookies = {}
    for item in cookie_str.split(';'):
        key, value = item.strip().split('=', 1)  # 1 means split only once
        cookies[key] = value
    return cookies
