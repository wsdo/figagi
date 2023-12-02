import glob
import os
from spacy.tokens import Doc
from spacy.language import Language
from pathlib import Path
from wasabi import msg

try:
    from PyPDF2 import PdfReader
except Exception:
    msg.warn("PyPDF2未安装")

def chunk_docs(
    raw_docs: list[Doc],
    nlp: Language,
    split_length: int = 150,
    split_overlap: int = 50,
) -> list[Doc]:
    """
    将一系列文档分割成更小的段落。
    参数:
        raw_docs : list[Doc] - 文档列表
        nlp : Language - spaCy NLP对象
        split_length : int - 分割长度（词、句子、段落）
        split_overlap : int - 分割时的重叠长度
    返回:
        list[Doc] - 分割后的文档列表
    """
    msg.info("开始分割过程")
    chunked_docs = []
    for doc in raw_docs:
        chunked_docs += chunk_doc(doc, nlp, split_length, split_overlap)
    msg.good(f"分割成功（总计 {len(chunked_docs)} 个段落）")
    return chunked_docs


def chunk_doc(
    doc: Doc, nlp: Language, split_length: int, split_overlap: int
) -> list[Doc]:
    """
    将单个文档分割成更小的段落。
    参数:
        doc : Doc - spaCy文档对象
        nlp : Language - spaCy NLP对象
        split_length : int - 分割长度
        split_overlap : int - 重叠长度
    返回:
        list[Doc] - 从原文档分割出的小段落列表
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
            end_idx = len(doc)  # 调整最后一个块的结束索引

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


def pdf_load_file(file_path: Path) -> dict:
    """
    加载PDF文件并以字典形式返回其内容。
    参数:
        file_path : Path - 文件路径
    返回:
        dict - 字典，包含文件名（键）和内容（值）
    """
    file_contents = {}
    file_types = [".pdf"]

    # 检查文件类型是否支持
    if file_path.suffix.lower() not in file_types:
        print(f"{file_path.suffix} 不支持。")
        return {}

    # 初始化一个变量来保存PDF的全部文本
    full_text = ""
    
    # 读取PDF文件
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:  # 检查是否成功提取了文本
                full_text += text + "\n\n"
    except Exception as e:
        print(f"读取文件 {file_path} 时出错：{e}")
        return {}

    # 将提取的文本存储在字典中
    file_contents[file_path.name] = full_text.strip()

    print(f"已加载文件：{file_path.name}")

    return file_contents