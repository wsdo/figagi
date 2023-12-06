#! .venv/bin/python
'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-22 13:29:06
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-26 16:21:15
Description: 
'''
from ai_assistant.load_env import load_env
load_env()

import openai
import inspect
from ai_assistant.config import config
# from langchain.llms import OpenAI
# from openai.api_requestor import APIRequestor

def main():
    # llm = OpenAI(temperature=0.5)
    pass
    


if __name__ == "__main__":
    main()
