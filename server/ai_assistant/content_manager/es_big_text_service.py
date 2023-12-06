'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-20 20:03:42
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-21 00:01:17
Description: 
'''
from .big_text import BigText
from abc import ABCMeta, abstractmethod
from .big_text_service import BigTextService
from elasticsearch import Elasticsearch
from ai_assistant.common.service_common import (is_insert_ok, dict_model,
    append_create_fields, append_update_fields, append_logic_delete_fileds)

class EsBigTextService(BigTextService):
    def __init__(self,
        es_url: str = None,
        es_index: str = None,
    ) -> None:
        super().__init__()
        self.es_url = es_url
        self.es_index = es_index
        self.es = Elasticsearch(hosts=es_url)

    def get_by_id(self, id: str) -> BigText:
        resp = self.es.get(index=self.es_index, id=id)
        c = BigText()
        source = resp['_source'] 
        for key, value in source.items():
            if (hasattr(c, key)):
                setattr(c, key, value)
        
        c.id = resp['_id']
        return c

    def create(self, obj: BigText) -> BigText:
        append_create_fields(obj)
        document = dict_model(obj)

        resp = self.es.index(index=self.es_index, 
            document=document)

        if (not is_insert_ok(resp['result'])):
            raise RuntimeError(f'create error: {resp["result"]}')
        
        obj.id = resp['_id']

        return obj

    def create_by_text(self, text: str) -> BigText:
        bt = BigText()
        bt.text = text
        
        return self.create(bt)

    def update(self, obj: BigText):
        append_update_fields(obj)
        doc = dict_model(obj)
        resp = self.es.index(index=self.es_index, id = obj.id, document=doc)

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
    