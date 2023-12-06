'''
Author: yuyingtao yuyingtao@agiclas.cn
Date: 2023-06-18 08:26:18
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-28 20:39:41
Description: 
'''
from typing import List, Dict, Optional, Literal, Tuple
from .content_service import ContentService
from ai_assistant.common.service_common import (is_insert_ok, dict_model,
    append_create_fields, append_update_fields, append_logic_delete_fileds)
from ai_assistant.content_manager.content import Content
from ai_assistant.utils.object import copyObjToObj

from .big_text_service import BigTextService

from elasticsearch import Elasticsearch
from datetime import datetime
from ai_assistant.utils.logger import create_logger

logger = create_logger('es_content_service')

class EsContentService(ContentService):
    def __init__(self,
        es_url: str,
        es_index: str,
        big_text_service: BigTextService
    ) -> None:
        super().__init__()
        self.es_url = es_url
        self.es_index = es_index
        self.es = Elasticsearch(hosts=es_url)
        self.bt_service = big_text_service

    def get_by_id(self, id: str) -> Content | None:
        try:
            resp = self.es.get(index=self.es_index, id=id)
            c = Content()
            source = resp['_source'] 
            for key, value in source.items():
                if (hasattr(c, key)):
                    setattr(c, key, value)
            
            c.id = resp['_id']
            return c
        except:
            return None
    
    def search_contents(self, last_created: datetime = datetime.max, size: int = 10, must: List[Dict] = [], filter: List[Dict] = [], sort_order: Literal["desc", 'asc'] = 'desc') -> List[Content]:
        query: Dict | None = None        

        if (must and len(must) > 0):
            query = {} if not query else query
            bool_node = query.get('bool') if 'bool' in query else {}
            query['bool'] = bool_node
            bool_node['must'] = must

        new_filter = filter.copy()
        new_filter.append({ "term": { "deleted":  0 } })
        query = {} if not query else query
        bool_node = query.get('bool') if 'bool' in query else {}
        query['bool'] = bool_node
        bool_node['filter'] = new_filter
        
        logger.info('search_contents, query: %s', query)
        resp = self.es.search(index=self.es_index, query=query, search_after=[last_created], size=size, sort={"created": sort_order})
        results = resp['hits']['hits']

        ret = []
        for result in results:
            c = Content()
            source = result['_source']
            for key, value in source.items():
                if (hasattr(c, key)):
                    setattr(c, key, value)

            c.id = result['_id']

            ret.append(c)

        return ret

    def search_contents_paged(self, last_id: str | None = None, size: int = 10, must: List[Dict] = [], filter: List[Dict] = [], sort_order: Literal["desc", 'asc'] = 'desc') -> List[Content]:
        if (last_id is None):
            return self.search_contents(size=size, must=must, filter=filter, sort_order=sort_order)

        content = self.get_by_id(last_id)
        if (content is None):
            return self.search_contents(size=size)

        return self.search_contents(last_created=content.created, must=must, filter=filter, size=size)

    def get_content_by_origin(self, origin: str) -> Optional[Content]:
        resp = self.search_contents(filter=[{"term": {"origin": origin}}])
        
        return resp[0] if len(resp) > 0 else None

    def create(self, content: Content, text: str) -> Content:
        bt = self.bt_service.create_by_text(text)

        content.text_id = bt.id
        append_create_fields(content)
        document = dict_model(content)

        resp = self.es.index(index=self.es_index, 
            document=document)

        if (not is_insert_ok(resp['result'])):
            raise RuntimeError(f'create error: {resp["result"]}')
        content.id = resp['_id']

        return content

    # 对于每个来源的文章，只需要收录一次
    def checkAndCreate(self, content: Content, text: str) -> Tuple[bool, Content]:
        old = self.get_content_by_origin(content.origin)
        if (old is not None):
            return (False, old)
        else:
            newobj = self.create(content=content, text=text)
            return (True, newobj)
            
    def update(self, content: Content):
        logger.info('update: %s', content.__dict__)
        full_content = self.get_by_id(content.id)
        if (full_content == None):
            raise RuntimeError(f'no content. id: {content.id}')

        copyObjToObj(content, full_content)
        append_update_fields(full_content)

        logger.info('update: full_content %s', full_content.__dict__)
        doc = dict_model(full_content)
        resp = self.es.index(index=self.es_index, id = full_content.id, document=doc)

        return resp

    def delete(self, id: str, logic = True):
        if logic:
            content = self.get_by_id(id)
            if (content == None):
                return
            append_logic_delete_fileds(content)
            self.update(content)
        else:
            self.es.delete(index=self.es_index, id=id)

    def get_text(self, content: Content):
        c = self.bt_service.get_by_id(content.text_id)

        if (c is None):
            return None

        return c.text
        