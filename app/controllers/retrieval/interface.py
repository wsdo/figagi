import weaviate
from weaviate import Client
from app.common.util import setup_client

class QueryEngine:
    """
    用于AGIAID查询引擎的接口。
    此类提供了与Weaviate数据库交互的基本方法。
    """

    client: Client = None

    def __init__(self):
        """
        构造函数，初始化查询引擎，并设置Weaviate客户端。
        """
        QueryEngine.client = setup_client()

    def query(self, query_string: str) -> tuple:
        raise NotImplementedError("query 方法必须由子类实现。")

    def retrieve_document(self, doc_id: str) -> dict:
        raise NotImplementedError("retrieve_document 方法必须由子类实现。")

    def retrieve_all_documents(self) -> list:
        raise NotImplementedError("retrieve_all_documents 方法必须由子类实现。")

    def get_client(self) -> Client:
        return QueryEngine.client
