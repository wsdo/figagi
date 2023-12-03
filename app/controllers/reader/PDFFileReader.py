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