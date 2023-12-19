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
    Split a series of documents into smaller chunks.
    Parameters:
        raw_docs : list[Doc] - List of documents
        nlp : Language - spaCy NLP object
        split_length : int - Chunk length (in words, sentences, paragraphs)
        split_overlap : int - Overlap length between chunks
    Returns:
        list[Doc] - List of chunked documents
    """
    msg.info("Starting chunking process")
    chunked_docs = []
    for doc in raw_docs:
        chunked_docs += chunk_doc(doc, nlp, split_length, split_overlap)
    msg.good(f"Successfully chunked ({len(chunked_docs)} in total)")
    return chunked_docs

def chunk_doc(
    doc: Doc, nlp: Language, split_length: int, split_overlap: int
) -> list[Doc]:
    """
    Split a single document into smaller chunks.
    Parameters:
        doc : Doc - spaCy document
        nlp : Language - spaCy NLP object
        split_length : int - Chunk length
        split_overlap : int - Overlap length between chunks
    Returns:
        list[Doc] - List of chunked documents
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
            end_idx = len(doc)  # Adjust the end position for the last chunk

        doc_chunk = nlp.make_doc(doc[start_idx:end_idx].text)
        doc_chunk.user_data = doc.user_data.copy()
        doc_chunk.user_data["_split_id"] = split_id_counter
        split_id_counter += 1

        doc_chunks.append(doc_chunk)

        # Exit loop if this is the last possible chunk
        if end_idx == len(doc):
            break

        i += split_length - split_overlap  # Move forward considering the overlap

    return doc_chunks

def process_file(file_path: Path) -> Dict:
    """
    Process a single file based on its type.
    Parameters:
        file_path : Path - Path to the file
    Returns:
        dict - Dictionary of file content
    """
    file_type = file_path.suffix.lower()
    if file_type in ['.pdf']:
        return pdf_load_file(file_path)
    elif file_type in ['.txt', '.md', '.mdx', '.json']:
        return text_load_file(file_path)
    else:
        msg.warn(f"Unsupported file type: {file_type}")
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
    Convert a list of strings to spaCy documents.
    Parameters:
        client : Client - Database client
        files : dict - Dictionary of file names and contents
        nlp : Language - spaCy NLP object
        doc_type : str - Document type, default is "Documentation"
    Returns:
        list[Doc] - List of spaCy documents
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
        msg.info(f"Converting {doc.user_data['doc_name']}")
        if not check_if_file_exits(client, file_name):
            raw_docs.append(doc)
        else:
            msg.warn(f"{file_name} already exists in the database")

    msg.good(f"Successfully loaded {len(raw_docs)} files")
    return raw_docs

def check_if_file_exits(client: Client, doc_name: str) -> bool:
    """
    Check if a file already exists in the database.
    Parameters:
        client : Client - Database client
        doc_name : str - Document name
    Returns:
        bool - Whether the file exists
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
