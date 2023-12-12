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

        print("===messages==",messages)
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
            .with_generate(
                grouped_task=f"您是RAG的聊天机器人，根据给定的上下文回答查询{query_string} 仅使用上下文提供的信息，务必用中文回答"
            )
            .with_additional(properties=["score"])
            .with_limit(1)
            .do()
        )

        if "data" not in query_results:
            raise Exception(query_results)

        results = query_results["data"]["Get"]["Chunk"]
        openai_res  = self.generate_response(query_string)
        return (results, openai_res)
    
    def openai_query(self, query_string,chat_histroy)-> tuple:

        # 获取当前查询的 Query
        last_content = query_string[-1]['content'] if query_string else None
        print("\n ==当前查询的问题===",last_content)
        # 通过向量数据库查询
        vector_query_results = (
            QueryEngine.client.query.get(
                class_name="Chunk",
                properties=["text", "doc_name", "chunk_id", "doc_uuid", "doc_type"],
            )
            .with_hybrid(query=last_content)
            # .with_additional(properties=["score"])
            .with_additional("score")
            .with_limit(1)
            .do()
        )

        # 向量数据库查询的结果
        vector_res = vector_query_results["data"]["Get"]["Chunk"]
        print("\n ==向量数据库查vector_query_results询的结果===",vector_query_results)
        print("\n ==向量数据库查询的结果===",vector_res)
        
        pre_query = f"{last_content}"

        for item in vector_res:
            # 确保 '_additional' 字典存在且包含 'score' 键
            if '_additional' in item and 'score' in item['_additional']:
                # 将 score 值转换为浮点数
                score = float(item['_additional']['score'])

                print("\n ====score====",score)
                if score > 0.0121:
                    pre_query = f"您是RAG的聊天机器人，根据给定的上下文{vector_res}, 回答查询{last_content} 仅使用上下文提供的信息，务必用中文回答"
                    print("\n ====pre_query====", pre_query)
                    break  # 如果不需要检查其他项，则退出循环       
        
        print("\n ====最终 pre_query====", pre_query)  # 检查循环结束后的 pre_query 值
        database_results = [
            {'role': 'user', 'content': pre_query}
        ]
        transformed_initial_data = [{'role': role, 'content': content} for role, content in chat_histroy]

        # 删除最后一个对象
        transformed_initial_data.pop()

        # 待合并的数组
        database_results = [
            {'role': 'user', 'content': pre_query}  # 假设 pre_query 已经定义
        ]

        # 合并两个列表
        merged_data = transformed_initial_data + database_results

        print("\n ===database_results===",database_results)
        print("\n ===chat_histroy===",chat_histroy)
        print("\n ===transformed_initial_data===",transformed_initial_data)
        print("\n ===merged_data===",merged_data)
        
        # 用向量数据库的结果，向 OpenAI 查询
        openai_res = self.generate_response(merged_data)
        print("\n ==openai查询的结果===",openai_res)
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