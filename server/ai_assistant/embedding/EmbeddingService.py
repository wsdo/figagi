'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-03 11:39:09
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-06-21 18:49:13
Description: 
'''
from typing import Literal, Any, Dict
from abc import ABCMeta, abstractmethod

from langchain.vectorstores.base import VectorStoreRetriever
from .content_embedding import ContentEmbedding
from ai_assistant.embedding.EsEmbeddingService import EsEmbeddingService
from ai_assistant.embedding.EmbeddingServiceInitData import EmbeddingServiceInitData

class EmbeddingService(metaclass=ABCMeta):
    def __init__(self, init: EmbeddingServiceInitData):
        self.config = init.config
        self.embedding = init.embedding
        self.vectors_store = None

    @abstractmethod
    def as_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
        pass

    @abstractmethod
    def add(self, embedding: ContentEmbedding) -> ContentEmbedding:
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

    @abstractmethod
    def edit(self, id: int, data: Dict):
        pass

    @staticmethod
    def load_embedding_service(type: Literal['es'], init: EmbeddingServiceInitData):
        return EsEmbeddingService(init)