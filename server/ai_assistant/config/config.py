'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-03 18:12:42
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-07-01 01:46:43
Description: main config
'''
import os
from ai_assistant.utils.logger import create_logger

logger = create_logger('config')

class Config:
    def __init__(self):
        self.ES_URL_PROTOCAL = os.getenv('ES_URL_PROTOCAL', 'http')
        self.ES_USER = os.getenv('ES_USER', '')
        self.ES_PASSWORD = os.getenv('ES_PASSWORD', '')
        self.ES_SECURITY = f'{self.ES_USER}:{self.ES_PASSWORD}@' if (self.ES_USER != '' and self.ES_PASSWORD != '') else ''
        self.ES_URL_HOST = os.getenv('ES_URL_HOST')

        self.ES_URL = f'{self.ES_URL_PROTOCAL}://{self.ES_SECURITY}{self.ES_URL_HOST}'

        self.DB_EMBEDDING = os.getenv('DB_EMBEDDING', 'aisearch')
        self.DB_CONTENT =  os.getenv('DB_CONTENT', 'content')
        self.DB_BIG_TEXT = os.getenv('DB_BIG_TEXT', 'bigtext')

        self.CANDIDATES_DIRECTORY = os.getenv('CANDIDATES_DIRECTORY', 'data/knowledge/candidates')
        self.FILES_DIRECTORY = os.getenv('FILES_DIRECTORY', 'data/knowledge/files')
        self.KNOWLEDGE_BASE_PATH = os.getenv('KNOWLEDGE_BASE_PATH', 'http://locahost:7777')

        self.LDAP_SERVER_URI = os.getenv('LDAP_SERVER_URI', '  ldap://39.106.15.22:3389')
        self.LDAP_DEFAULT_ADMIN = os.getenv('LDAP_DEFAULT_ADMIN', 'cn=admin,dc=agiclass,dc=ai')
        self.LDAP_ADMIN_PASSWORD = os.getenv('LDAP_ADMIN_PASSWORD', 'some_password')
        self.LDAP_SEARCH_BASE = os.getenv('LDAP_SEARCH_BASE', 'ou=people, dc=agiclass, dc=ai')
        self.BYPASS_AUTH = int(os.getenv('BYPASS_AUTH', '0')) == 1

        self.SERVER_TOKEN = os.getenv('SERVER_TOKEN', 'server_token')
        self.RUN_SERVER_RELOAD = int(os.getenv('RUN_SERVER_RELOAD', '0')) == 1

config = Config()