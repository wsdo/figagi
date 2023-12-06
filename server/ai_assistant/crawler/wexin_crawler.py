'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-27 14:43:53
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-29 02:01:53
Description: 
'''
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from ai_assistant.wx_spider.wx_spider.spiders.wx_article_list  import WxArticleListSpider
from ai_assistant.wx_spider.wx_spider.spiders.wx_article import WxArticleSpider
from scrapy.signalmanager import dispatcher
from ai_assistant.utils.logger import create_logger
import concurrent.futures

logger = create_logger('wexin_crawler')


def crawl_wx_platform_article_list(fake_id, token, cookie, begin = 0):
    settings = {
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'DOWNLOAD_DELAY': 15,
        'REACTOR_THREADPOOL_MAXSIZE': 10,
    }
    p = CrawlerProcess(settings=settings)
    results = []
    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    crawler = p.create_crawler(WxArticleListSpider)
    dispatcher.connect(crawler_results, signal=signals.item_scraped, sender=crawler)
    p.crawl(crawler, token=token, fake_id=fake_id, cookie=cookie, begin=begin)
    p.start()

    dispatcher.disconnect(crawler_results, signal=signals.item_scraped, sender=crawler)
    logger.info('len of article list: %s', len(results))
    return results

def crawl_wx_platform_article(msg_list):
    settings = {
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'DOWNLOAD_DELAY': 1,
    }

    p = CrawlerProcess(settings=settings)
    results = []
    def crawler_results(signal, sender, item, response, spider):
        results.append(item)
    crawler = p.create_crawler(WxArticleSpider)
    dispatcher.connect(crawler_results, signal=signals.item_scraped, sender=crawler)
    p.crawl(crawler, msg_list=msg_list)
    p.start()

    dispatcher.disconnect(crawler_results, signal=signals.item_scraped, sender=crawler)

    logger.info('len of article content: %s', len(results))
    return results

def crawl_wx_platform(fake_id, token, cookie, begin = 0):
    msg_list = []
    with concurrent.futures.ProcessPoolExecutor(1) as executor:
        p = executor.submit(crawl_wx_platform_article_list, fake_id, token, cookie, begin)
        msg_list = p.result()

    articles = []
    with concurrent.futures.ProcessPoolExecutor(1) as executor:
        p = executor.submit(crawl_wx_platform_article, msg_list)
        articles = p.result()

    return articles