'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-02 14:14:17
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-07-11 14:15:18
Description: 
'''
from typing import List
from queue import Queue
import os
import json
from datetime import datetime
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from ai_assistant.utils.object import Object
from ai_assistant.embedding.EmbeddingService import EmbeddingService
from ai_assistant.config.config import Config
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from ai_assistant.app.AsyncQueueStreamingOutCallbackHandler import AsyncQueueStreamingOutCallbackHandler


from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

class LangChainService:
    queue_done = object()

    def __init__(self, config: Config, temperature):
        self.llm = OpenAI(temperature=temperature)
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature, streaming=True)
        self.config = config
        
        init_data = Object()
        init_data.embedding = OpenAIEmbeddings()
        init_data.config = config
        self.embedding_service = EmbeddingService.load_embedding_service(type='es', init=init_data)
    
    async def asearch_with_knowledge(self,
                        query: str,
                        top_k: float = 10,
                        q: Queue | None = None,
                        chat_history: List[str] = []):
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("你是一个 AI 学习助手。基于以下已知信息，专业和详细的回答问题。如果根据已知信息无法得到答案，可以使用你知道的其他信息回答，但不允许在答案中添加编造成分。答案请使用中文。"),
            HumanMessagePromptTemplate.from_template("""
已知信息：
{context}
问题：
{question}
""")
        ])

        callbacks = [StreamingStdOutCallbackHandler()]

        if q is not None:
            queueHandler = AsyncQueueStreamingOutCallbackHandler(q)
            callbacks.append(queueHandler)
            

        knowledge_chain = RetrievalQA.from_llm(
            llm=self.chat,
            retriever=self.embedding_service.vectors_store.as_retriever(
                search_kwargs={"k": top_k}),
            prompt=prompt,
            verbose=True)

        knowledge_chain.return_source_documents = True
        result = await knowledge_chain.acall({ 'question': query, 'query': query }, callbacks=callbacks)
        q.put(LangChainService.queue_done)

        return result

    def search_with_knowledge(self,
                        query: str,
                        top_k: float,
                        callbacks=[StreamingStdOutCallbackHandler()],
                        chat_history: List[str] = []):

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("你是一个 AI 学习助手。基于以下已知信息，专业和详细的回答问题。如果根据已知信息无法得到答案，可以使用你知道的其他信息回答，但不允许在答案中添加编造成分。答案请使用中文。"),
            HumanMessagePromptTemplate.from_template("""
已知信息：
{context}
问题：
{question}
""")
        ])

        knowledge_chain = RetrievalQA.from_llm(
            llm=self.chat,
            retriever=self.embedding_service.vectors_store.as_retriever(
                search_kwargs={"k": top_k}),
            prompt=prompt,
            verbose=True)

        knowledge_chain.return_source_documents = True

        result = knowledge_chain({ 'question': query, 'query': query }, callbacks=callbacks)

        print('langchain result', result)

        return result

    def add_file_embedding(self, file_name: str, contents: List[str], source: str, file_type: str, content_id = '', content_type = '', content_category = ''):
        docs = []
        for content in contents:
            doc = Object()
            doc.page_content = content
            doc.metadata = {
                "source": source,
                "content_type": content_type,
                "file_type": file_type,
                "content_id": content_id,
                "title": file_name,
                "content_category": content_category,
                "created": datetime.now(),
                "updated": datetime.now(),
            }
            docs.append(doc)

        self.embedding_service.vectors_store.add_documents(documents=docs)

    def ask_chat_gpt(input):
        llm = OpenAI(temperature=0.9, allowed_special='all', model_name="gpt-3.5-turbo")
        text = input
        ret = llm(text)
        return ret