'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-03 20:14:43
LastEditors: moemoefish moemoefish@qq.com
LastEditTime: 2023-05-11 20:59:39
Description: 获取文件内容的工具
'''

import PyPDF2
import docx
from langdetect import detect
from typing import Tuple,List

class FileContent:
    @staticmethod
    def extract_file(file_path) -> Tuple[List[str], str]:
        if file_path.endswith('.pdf'):
            contents, lang = FileContent.extract_pdf_file(file_path)
        elif file_path.endswith('.txt') or file_path.endswith('.html'):
            contents, lang = FileContent.extract_txt_file(file_path)
        elif file_path.endswith('.docx'):
            contents, lang = FileContent.extract_docx_file(file_path)
        else:
            raise RuntimeError('not support file type')

        return contents, lang

    @staticmethod
    def extract_txt_file(file_path) -> Tuple[List[str], str]:
        with open(file_path, 'r', encoding='utf-8') as f:
            contents = [text.strip() for text in f.readlines() if text.strip()]
            lang = detect('\n'.join(contents))
        return contents, lang[0:2]

    def extract_pdf_file(file_path) -> Tuple[List[str], str]:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            contents = []
            for page in pdf_reader.pages:
                page_text = page.extract_text().strip()
                raw_text = [text.strip() for text in page_text.splitlines() if text.strip()]
                new_text = ''
                for text in raw_text:
                    new_text += text
                    if text[-1] in ['.', '!', '?', '。', '！', '？', '…', ';', '；', ':', '：', '”', '’', '）', '】', '》', '」',
                                    '』', '〕', '〉', '》', '〗', '〞', '〟', '»', '"', "'", ')', ']', '}']:
                        contents.append(new_text)
                        new_text = ''
                if new_text:
                    contents.append(new_text)
        lang = detect('\n'.join(contents))
        return contents, lang[0:2]


    def extract_docx_file(file_path) -> Tuple[List[str], str]:
        document = docx.Document(file_path)
        contents = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
        lang = detect('\n'.join(contents))

        return contents, lang[0:2]