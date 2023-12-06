'''
Author: moemoefish moemoefish@qq.com
Date: 2023-06-14 01:00:19
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-18 21:28:22
Description: 
'''
import os
from dotenv import load_dotenv

def load_env():
    # This one is for the Development Env
    env = os.getenv('ENVIRONMENT', 'dev')
    env = '' if env == '' else f'.{env}'
    dotenv_path = f'.env{env}'
    load_dotenv(dotenv_path=dotenv_path)
    load_dotenv(dotenv_path='.env', override=True)

    print(f'ENVIRONMENT: {env}')