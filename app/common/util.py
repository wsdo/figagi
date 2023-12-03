import hashlib
import ssl
import os

import openai
import weaviate
from weaviate import Client
from typing import Optional
from spacy.tokens import Doc
from weaviate.embedded import EmbeddedOptions

from wasabi import msg


def setup_client() -> Optional[Client]:
    """
    设置 Weaviate 客户端。

    @returns Optional[Client] - 返回 Weaviate 客户端实例
    """
    msg.info("正在设置客户端")

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    weaviate_url = os.environ.get("WEAVIATE_URL", "")
    weaviate_key = os.environ.get("WEAVIATE_API_KEY", "")

    if openai_key == "":
        msg.fail("OPENAI_API_KEY 环境变量未设置")
        return None

    elif weaviate_url == "":
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        msg.info("WEAVIATE_URL 环境变量未设置，使用 Weaviate Embedded")
        client = weaviate.Client(
            additional_headers={"X-OpenAI-Api-Key": openai.api_key},
            embedded_options=EmbeddedOptions(
                persistence_data_path="./.agiaid/local/share/",
                binary_path="./.agiaid/cache/weaviate-embedded",
            ),
        )
        msg.good("客户端已连接到本地 Weaviate 服务器")
        return client

    elif weaviate_key == "":
        msg.warn("WEAVIATE_API_KEY 环境变量未设置")

    openai.api_key = openai_key
    url = weaviate_url
    auth_config = weaviate.AuthApiKey(api_key=weaviate_key)

    client = weaviate.Client(
        url=url,
        additional_headers={"X-OpenAI-Api-Key": openai.api_key},
        auth_client_secret=auth_config,
    )

    msg.good("客户端已连接到 Weaviate 集群")

    return client


def hash_string(text: str) -> str:
    """
    对字符串进行哈希处理。

    @parameter text : str - 要进行哈希处理的字符串
    @returns str - 哈希处理后的字符串
    """
    sha256 = hashlib.sha256()
    sha256.update(text.encode())
    return str(sha256.hexdigest())


def import_documents(client: Client, documents: list[Doc]) -> dict:
    """
    将文档列表导入 Weaviate 客户端，并返回块匹配的 UUID 列表。

    @parameter client : Client - Weaviate 客户端
    @parameter documents : list[Document] - 完整文档的列表
    @returns dict - 返回 UUID 列表
    """
    doc_uuid_map = {}

    with client.batch as batch:
        batch.batch_size = 100
        for i, d in enumerate(documents):
            msg.info(
                f"({i+1}/{len(documents)}) 正在导入文档 {d.user_data['doc_name']}"
            )

            properties = {
                "text": str(d.text),
                "doc_name": str(d.user_data["doc_name"]),
                "doc_type": str(d.user_data["doc_type"]),
                "doc_link": str(d.user_data["doc_link"]),
            }

            uuid = client.batch.add_data_object(properties, "Document")
            uuid_key = str(d.user_data["doc_hash"]).strip().lower()
            doc_uuid_map[uuid_key] = uuid

    msg.good("所有文档已导入")
    return doc_uuid_map


def import_chunks(client: Client, chunks: list[Doc], doc_uuid_map: dict) -> None:
    """
    将文档块列表导入 Weaviate 客户端，并使用文档的 UUID 列表进行匹配。

    @parameter client : Client - Weaviate 客户端
    @parameter chunks : list[Document] - 文档块的列表
    @parameter doc_uuid_map : dict - 文档块所属文档的 UUID 列表
    @returns None
    """
    with client.batch as batch:
        batch.batch_size = 100
        for i, d in enumerate(chunks):
            msg.info(
                f"({i+1}/{len(chunks)}) 正在导入 {d.user_data['doc_name']} 的块 ({d.user_data['_split_id']})"
            )

            uuid_key = str(d.user_data["doc_hash"]).strip().lower()
            uuid = doc_uuid_map[uuid_key]

            properties = {
                "text": str(d.text),
                "doc_name": str(d.user_data["doc_name"]),
                "doc_uuid": uuid,
                "doc_type": str(d.user_data["doc_type"]),
                "chunk_id": int(d.user_data["_split_id"]),
            }

            client.batch.add_data_object(properties, "Chunk")

    msg.good("所有块已导入")
