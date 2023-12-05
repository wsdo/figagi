from app.controllers.retrieval.interface import QueryEngine
from typing import Optional
import json
from wasabi import msg
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

class RetrieverEngine(QueryEngine):

    def generate_response(self, messages):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        return response
    
    def query(self, query_string: str) -> tuple:
        query_results = (
            QueryEngine.client.query.get(
                class_name="Chunk",
                properties=["text", "doc_name", "chunk_id", "doc_uuid", "doc_type"],
            )
            .with_hybrid(query=query_string)
            # .with_generate(
            #     grouped_task=f"您是RAG的聊天机器人，根据给定的上下文回答查询{query_string} 仅使用上下文提供的信息，务必用中文回答"
            # )
            .with_additional(properties=["score"])
            .with_limit(1)
            .do()
        )

        if "data" not in query_results:
            raise Exception(query_results)

        results = query_results["data"]["Get"]["Chunk"]
        # pre_query = f"您是RAG的聊天机器人，根据给定的上下文{results}, 回答查询{query_string} 仅使用上下文提供的信息，务必用中文回答"

        openai_res  = self.generate_response(query_string)
        return (results, openai_res)
    
    def openai_query(self, query_string)-> tuple:

        # 获取当前查询的 Query
        last_content = query_string[-1]['content'] if query_string else None

        # 通过向量数据库查询
        vector_query_results = (
            QueryEngine.client.query.get(
                class_name="Chunk",
                properties=["text", "doc_name", "chunk_id", "doc_uuid", "doc_type"],
            )
            .with_hybrid(query=last_content)
            # .with_generate(
            #     grouped_task=f"您是RAG的聊天机器人，根据给定的上下文回答查询{query_string} 仅使用上下文提供的信息，务必用中文回答"
            # )
            .with_additional(properties=["score"])
            .with_limit(1)
            .do()
        )

        # 向量数据库查询的结果
        vector_res = vector_query_results["data"]["Get"]["Chunk"]

        pre_query = f"您是RAG的聊天机器人，根据给定的上下文{vector_res}, 回答查询{last_content} 仅使用上下文提供的信息，务必用中文回答"
        database_results = [
            {'role': 'user', 'content': pre_query}
        ]
        
        # 合并这两个数组
        combined_messages = query_string + database_results
        
        # 用向量数据库的结果，向 OpenAI 查询
        openai_res = self.generate_response(combined_messages)
        return openai_res

    def retrieve_document(self, doc_id: str) -> dict:

        document = QueryEngine.client.data_object.get_by_id(
            doc_id,
            class_name="Document",
        )
        return document

    def retrieve_all_documents(self) -> list:
        query_results = (
            QueryEngine.client.query.get(
                class_name="Document", properties=["doc_name", "doc_type", "doc_link"]
            )
            .with_additional(properties=["id"])
            .with_limit(1000)
            .do()
        )

        print(query_results,"=====")
        results = query_results["data"]["Get"]["Document"]
        return results

    def search_documents(self, query: str) -> list:
        query_results = (
            QueryEngine.client.query.get(
                class_name="Document", properties=["doc_name", "doc_type", "doc_link"]
            )
            .with_bm25(query, properties=["doc_name"])
            .with_additional(properties=["id"])
            .with_limit(20)
            .do()
        )
        results = query_results["data"]["Get"]["Document"]
        return results