#! .venv/bin/python
'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-02 14:11:04
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-28 20:34:10
Description: 
'''
import os
import shutil
from datetime import datetime
from pathlib import Path
from ai_assistant.config.config import config
from ai_assistant.crawler.FileContent import FileContent
from ai_assistant.app.LangChainService import LangChainService


def embedding_files():
    candidates = os.walk(config.CANDIDATES_DIRECTORY)

    service = LangChainService(config=config, temperature=0.9)
    todayStr = datetime.now().strftime('%Y-%m-%d')
    directory = f'{config.FILES_DIRECTORY}/{todayStr}'

    for path,_,file_list in candidates:
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            
            try:
                contents, _ = FileContent.extract_file(file_path)
                service.add_file_embedding(file_name=file_name, contents=contents,
                                           source= f'{todayStr}/{file_name}', file_type='txt')
                Path(directory).mkdir(parents=True, exist_ok=True)
                shutil.move(file_path, directory)
            except RuntimeError as err:
                print(err)

def main():
    embedding_files()

if __name__ == '__main__':
    main()
