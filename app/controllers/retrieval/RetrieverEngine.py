from app.controllers.retrieval.interface import QueryEngine
from openai import OpenAI
from typing import Optional
import json
from wasabi import msg

client = OpenAI()

class RetrieverEngine(QueryEngine):

    def generate_response(self, messages):
        print("===generate_response==",messages)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        print("===QueryEngine==",response)
        # return response
        return response.choices[0].message.content


    def query(self, query_string: str) -> tuple:
        """Execute a query to a receive specific chunks from Weaviate
        @parameter query_string : str - Search query
        @returns tuple - (system message, iterable list of results)
        """
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

        # print("====",openai_res)

        if "data" not in query_results:
            raise Exception(query_results)

        results = query_results["data"]["Get"]["Chunk"]
        # pre_query = f"您是RAG的聊天机器人，根据给定的上下文{results}, 回答查询{query_string} 仅使用上下文提供的信息，务必用中文回答"
        print('query_string',query_string)
        openai_res  = self.generate_response(query_string)
        # system_msg = results[0]["_additional"]["generate"]["error"]
        return (results, openai_res)
    
    def openai_query(self, query_string)-> tuple:
        """Execute a query to a receive specific chunks from Weaviate
        @parameter query_string : str - Search query
        @returns tuple - (system message, iterable list of results)
        """
        # 获取最后的查询
        # last_content = query_string[-1]['content']

        print("===query_string====",query_string)

        # Extracting the last content
        last_content = query_string[-1]['content'] if query_string else None


        print("===last_content====",last_content)

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
        # print("====",openai_res)

        # if "data" not in query_results:
            # raise Exception(query_results)

        vector_res = vector_query_results["data"]["Get"]["Chunk"]
        print("===vector_query_results====",vector_res)
        # pre_query = f"您是RAG的聊天机器人，根据给定的上下文{results}, 回答查询{query_string} 仅使用上下文提供的信息，务必用中文回答"
        print("===query_string===",query_string)

        database_results = [
            {'role': 'user', 'content': str(vector_res)}
        ]
        
        # 合并这两个数组
        combined_messages = query_string + database_results
        print('combined_messages',combined_messages)
        # 用向量数据库的结果，向 OpenAI 查询
        openai_res = self.generate_response(combined_messages)

        # 现在 combined_messages 包含了来自数据库和原始消息的所有内容
        # 接下来可以将 combined_messages 传递给 OpenAI


        print('===query_results=====',openai_res)

        # system_msg = results[0]["_additional"]["generate"]["error"]
        return openai_res

    def retrieve_document(self, doc_id: str) -> dict:
        """Return a document by it's ID (UUID format) from Weaviate
        @parameter doc_id : str - Document ID
        @returns dict - Document dict
        """
        document = QueryEngine.client.data_object.get_by_id(
            doc_id,
            class_name="Document",
        )
        return document

    def retrieve_all_documents(self) -> list:
        """Return all documents from Weaviate
        @returns list - Document list
        """
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
        """Search for documents from Weaviate
        @parameter query_string : str - Search query
        @returns list - Document list
        """
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