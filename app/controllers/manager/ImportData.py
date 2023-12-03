import os
from pathlib import Path
from wasabi import msg
import spacy
from app.common.util import setup_client, import_documents, import_chunks
from app.controllers.reader.ProcessingHub import process_file, process_directory, chunk_docs, convert_files
from app.controllers.schema.init_schema import init_schema
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def ImportData(path_str: str, model: str) -> None:
    """
    导入数据并处理。

    参数:
    path_str (str): 数据文件或目录的路径。
    model (str): 使用的模型名称。

    返回:
    None
    """
    data_path = Path(path_str)
    msg.divider("Starting data import")
    
    # 初始化NLP模型
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")

    # 设置客户端
    client = setup_client()
    if not client:
        msg.fail("Client setup failed")
        return

    # 初始化数据库模式
    if not client.schema.exists("Document"):
        init_schema(model)
    msg.info("All schemas available")

    # 处理文件或目录
    file_contents = {}
    if data_path.is_file():
        file_contents = process_file(data_path)
    else:
        file_contents = process_directory(data_path)

    # 导入文档和数据块
    if file_contents:
        documents = convert_files(client, file_contents, nlp=nlp)
        if documents:
            chunks = chunk_docs(documents, nlp)
            uuid_map = import_documents(client=client, documents=documents)
            import_chunks(client=client, chunks=chunks, doc_uuid_map=uuid_map)

    # 停止嵌入式数据库
    if client._connection.embedded_db:
        msg.info("Stopping Weaviate Embedded")
        client._connection.embedded_db.stop()
