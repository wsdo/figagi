'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-06-19 19:48:18
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-25 18:12:51
Description: 
'''
from typing import Dict, Mapping
from dataclasses import dataclass
from datetime import datetime

RESULT_CREATED = 'created'

def is_insert_ok(result):
    return result  == RESULT_CREATED

def dict_model(model: object):
    model_dict: Dict = vars(model) 

    for key, value in list(model_dict.items()):
        if value == None:
            model_dict.pop(key)

    return model_dict

def append_update(doc: Mapping) -> Mapping:
    doc["updated"] = datetime.now()

    return doc

def append_update_fields(doc: object) -> object:
    if (hasattr(doc, 'updated')):
        doc.updated = datetime.now()

    return doc

def append_create_fields(doc: object) -> object:
    if (hasattr(doc, 'deleted')):
        doc.deleted = 0
    if (hasattr(doc, 'created')):
        doc.created = datetime.now()
    if (hasattr(doc, 'updated')):
        doc.updated = datetime.now()

    return doc

def append_logic_delete_fileds(doc: object) -> object:
    if (hasattr(doc, 'deleted')):
        doc.deleted = int(datetime.now().timestamp() * 1000)