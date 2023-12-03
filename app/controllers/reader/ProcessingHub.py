from pathlib import Path
from typing import Dict
from wasabi import msg
from weaviate import Client
from app.common.util import hash_string
from spacy.tokens import Doc
from spacy.language import Language
import glob
from app.controllers.reader.PDFFileReader import (
    pdf_load_file
) 
from app.controllers.reader.TextFileReader import (
    text_load_file
) 

def chunk_docs(
    raw_docs: list[Doc],
    nlp: Language,
    split_length: int = 150,
    split_overlap: int = 50,
) -> list[Doc]:
    """
    将一系列文档分割成小块。
    参数:
        raw_docs : list[Doc] - 文档列表
        nlp : Language - spaCy NLP对象
        split_length : int - 块长度（词、句子、段落）
        split_overlap : int - 块之间的重叠长度
    返回:
        list[Doc] - 分割后的文档列表
    """
    msg.info("开始分割过程")
    chunked_docs = []
    for doc in raw_docs:
        chunked_docs += chunk_doc(doc, nlp, split_length, split_overlap)
    msg.good(f"分割成功（总计 {len(chunked_docs)}）")
    return chunked_docs

def chunk_doc(
    doc: Doc, nlp: Language, split_length: int, split_overlap: int
) -> list[Doc]:
    """
    将单个文档分割成小块。
    参数:
        doc : Doc - spaCy文档
        nlp : Language - spaCy NLP对象
        split_length : int - 块长度
        split_overlap : int - 块之间的重叠长度
    返回:
        list[Doc] - 分割后的文档块列表
    """
    if split_length > len(doc) or split_length < 1:
        return []

    if split_overlap >= split_length:
        return []

    doc_chunks = []
    i = 0
    split_id_counter = 0
    while i < len(doc):
        start_idx = i
        end_idx = i + split_length
        if end_idx > len(doc):
            end_idx = len(doc)  # 调整最后一个块的结束位置

        doc_chunk = nlp.make_doc(doc[start_idx:end_idx].text)
        doc_chunk.user_data = doc.user_data.copy()
        doc_chunk.user_data["_split_id"] = split_id_counter
        split_id_counter += 1

        doc_chunks.append(doc_chunk)

        # 如果这是最后一个可能的块，则退出循环
        if end_idx == len(doc):
            break

        i += split_length - split_overlap  # 考虑重叠部分向前移动

    return doc_chunks

def process_file(file_path: Path) -> Dict:
    """
    根据文件类型处理单个文件。
    参数:
        file_path : Path - 文件路径
    返回:
        dict - 文件内容的字典
    """
    file_type = file_path.suffix.lower()
    if file_type in ['.pdf']:
        return pdf_load_file(file_path)
    elif file_type in ['.txt', '.md', '.mdx', '.json']:
        return text_load_file(file_path)
    else:
        msg.warn(f"不支持的文件类型: {file_type}")
        return {}

def process_directory(dir_path: Path) -> Dict:
    file_contents = {}
    dir_path_str = str(dir_path)
    file_types = [".pdf",".md",".json",".txt"]

    for file_type in file_types:
        files = glob.glob(f"{dir_path_str}/**/*{file_type}", recursive=True)
        for file_path in files:
            file_path_obj = Path(file_path)
            msg.info(f"Reading {file_path}")
            file_content = process_file(file_path_obj)
            if file_content:
                file_contents.update(file_content)

    msg.good(f"Loaded {len(file_contents)} files")
    return file_contents

def convert_files(
    client: Client, files: dict, nlp: Language, doc_type: str = "Documentation"
) -> list[Doc]:
    """
    将字符串列表转换为spaCy文档列表。
    参数:
        client : Client - 数据库客户端
        files : dict - 文件名和内容的字典
        nlp : Language - spaCy NLP对象
        doc_type : str - 文档类型，默认为"Documentation"
    返回:
        list[Doc] - spaCy文档列表
    """
    raw_docs = []
    for file_name, file_content in files.items():
        doc = nlp(file_content)
        doc.user_data = {
            "doc_name": file_name,
            "doc_hash": hash_string(file_name),
            "doc_type": doc_type,
            "doc_link": "",
        }
        msg.info(f"转换 {doc.user_data['doc_name']}")
        if not check_if_file_exits(client, file_name):
            raw_docs.append(doc)
        else:
            msg.warn(f"{file_name} 已经存在于数据库中")

    msg.good(f"成功加载 {len(raw_docs)} 个文件")
    return raw_docs

def check_if_file_exits(client: Client, doc_name: str) -> bool:
    """
    检查文件是否已存在于数据库中。
    参数:
        client : Client - 数据库客户端
        doc_name : str - 文档名
    返回:
        bool - 文件是否存在
    """
    results = (
        client.query.get(
            class_name="Document",
            properties=[
                "doc_name",
            ],
        )
        .with_where(
            {
                "path": ["doc_name"],
                "operator": "Equal",
                "valueText": doc_name,
            }
        )
        .with_limit(1)
        .do()
    )

    return bool(results["data"]["Get"]["Document"])
