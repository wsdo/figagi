'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-03 11:41:59
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-06-27 02:52:31
Description: elastic search embedding
'''
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from ai_assistant.embedding.EmbeddingServiceInitData import EmbeddingServiceInitData
from .content_embedding import ContentEmbedding

class EsEmbeddingService():
    def __init__(self, init: EmbeddingServiceInitData):
        self.config = init.config
        self.embedding  = init.embedding
        self.es_url = self.config.ES_URL
        self.es_index = self.config.DB_EMBEDDING
        self.vectors_store = ElasticVectorSearch(elasticsearch_url=self.es_url, index_name=self.es_index, embedding=self.embedding)

    def add(self, embedding: ContentEmbedding) -> ContentEmbedding:
        pass
