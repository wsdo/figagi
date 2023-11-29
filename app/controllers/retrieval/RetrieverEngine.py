from app.controllers.retrieval.interface import QueryEngine

from typing import Optional
import json
from wasabi import msg


class RetrieverEngine(QueryEngine):
    def query(self, query_string: str, model: str = None) -> tuple:
        """Execute a query to a receive specific chunks from Weaviate
        @parameter query_string : str - Search query
        @returns tuple - (system message, iterable list of results)
        """

        if results:
            return (system_msg, results)

        query_results = (
            QueryEngine.client.query.get(
                class_name="Chunk",
                properties=["text", "doc_name", "chunk_id", "doc_uuid", "doc_type"],
            )
            .with_hybrid(query=query_string)
            .with_generate(
                grouped_task=f"You are a chatbot for RAG, answer the query {query_string} based on the given context. Only use information provided in the context. Only if asked or required provide code examples based on the topic at the end of your answer encapsulated with ```programming-language ```"
            )
            .with_additional(properties=["score"])
            .with_limit(8)
            .do()
        )

        if "data" not in query_results:
            raise Exception(query_results)

        results = query_results["data"]["Get"]["Chunk"]

        if results[0]["_additional"]["generate"]["error"]:
            system_msg = results[0]["_additional"]["generate"]["error"]
        else:
            system_msg = results[0]["_additional"]["generate"]["groupedResult"]
            self.add_semantic_cache(query_string, results, system_msg)

        return (system_msg, results)

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