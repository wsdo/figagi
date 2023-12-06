'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-05 14:53:48
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-07-04 02:01:23
Description: webapp 页面 ui 层数据处理
'''
from typing import List
from queue import Queue
from ai_assistant.app.LangChainService import LangChainService
from ai_assistant.utils.url_utils import url_join
from anyio import start_blocking_portal

RECOMMEND_MAX_LENGHT = 5


class WebAppService:
    def __init__(self, config):
        self.config = config
        self.lc_service = LangChainService(config=config, temperature=0.6)

    def predict_yield(self, query, chatHistory: List):
        content = ''
        chatHistory.append((None, content))
        with start_blocking_portal() as portal:
            q = Queue()
            resp = portal.start_task_soon(self.lc_service.asearch_with_knowledge, query, 10, q)

            while True:
                next_token = q.get(True, timeout=20)
                if next_token is LangChainService.queue_done:
                    break
                
                content += next_token
                chatHistory.pop()
                chatHistory.append((None, content))
                yield chatHistory

            ret = resp.result()
        
            recommends = []

            doc_set = set()
            def check_doc_existed(doc):
                title = doc.metadata.get('title')
                if (title in doc_set):
                    return False
                doc_set.add(title)
                return True
                
            source_documents = [doc for doc in ret.get('source_documents') if check_doc_existed(doc)]
            for doc in source_documents:
                title = doc.metadata.get('title')
                link = doc.metadata.get('source')

                if (title is None or link is None):
                    continue

                link = url_join(self.config.KNOWLEDGE_BASE_PATH, link)

                # recommends.append(f'[{title}]({link})')
                recommends.append(f'<li><a class="recomm-item" target="_blank" rel="noreferrer" href="{link}">{title}</a></li>')
                if (len(recommends) >= RECOMMEND_MAX_LENGHT):
                    break

            recommands_str = ''.join(recommends)
            recommands_str = f'<ol class="recomm-list">{recommands_str}</ol>'
            recommand_base = '相关推荐：'
            
            
            bot_message = f'{recommand_base}{recommands_str}' if len(recommends) > 0 else result
            content += '\n\n'
            content += bot_message
            chatHistory.pop()
            chatHistory.append((None, content))
            yield chatHistory


    def predict(self, query, chatHistory):
        ret = self.lc_service.search_with_knowledge(query=query, top_k = 10)
        result = ret.get('result').strip()
        recommends = []

        doc_set = set()
        def check_doc_existed(doc):
            title = doc.metadata.get('title')
            if (title in doc_set):
                return False
            doc_set.add(title)
            return True
            
        source_documents = [doc for doc in ret.get('source_documents') if check_doc_existed(doc)]
        for doc in source_documents:
            title = doc.metadata.get('title')
            link = doc.metadata.get('source')

            if (title is None or link is None):
                continue

            link = url_join(self.config.KNOWLEDGE_BASE_PATH, link)

            # recommends.append(f'[{title}]({link})')
            recommends.append(f'<li><a class="recomm-item" target="_blank" rel="noreferrer" href="{link}">{title}</a></li>')
            if (len(recommends) >= RECOMMEND_MAX_LENGHT):
                break

        recommands_str = ''.join(recommends)
        recommands_str = f'<ol class="recomm-list">{recommands_str}</ol>'
        recommand_base = '相关推荐：'
        
         
        bot_message = f'{result}\n\n{recommand_base}{recommands_str}' if len(recommends) > 0 else result

        chatHistory.append((None, bot_message))
        
        return chatHistory
    