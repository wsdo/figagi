from pathlib import Path
from typing import Dict
from wasabi import msg
from weaviate import Client
from app.common.util import hash_string
from spacy.tokens import Doc
from spacy.language import Language
from app.controllers.reader.PDFFileReader import (
    pdf_load_file, pdf_load_directory
) 
from app.controllers.reader.TextFileReader import (
    text_load_file, text_load_directory
) 

def chunk_docs(
    raw_docs: list[Doc],
    nlp: Language,
    split_length: int = 150,
    split_overlap: int = 50,
) -> list[Doc]:
    """Splits a list of docs into smaller chunks
    @parameter raw_docs : list[Doc] - List of docs
    @parameter split_length : int - Chunk length (words, sentences, paragraphs)
    @parameter split_overlap : int - Overlapping words, sentences, paragraphs
    @returns list[Doc] - List of splitted docs
    """
    msg.info("Starting splitting process")
    chunked_docs = []
    for doc in raw_docs:
        chunked_docs += chunk_doc(doc, nlp, split_length, split_overlap)
    msg.good(f"Successful splitting (total {len(chunked_docs)})")
    return chunked_docs

def chunk_doc(
    doc: Doc, nlp: Language, split_length: int, split_overlap: int
) -> list[Doc]:
    """Splits a doc into smaller chunks
    @parameter doc : Doc - spaCy Doc
    @parameter nlp : Language - spaCy NLP object
    @parameter split_length : int - Chunk length (words, sentences, paragraphs)
    @parameter split_overlap : int - Overlapping words, sentences, paragraphs
    @returns list[Doc] - List of chunks from original doc
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
            end_idx = len(doc)  # Adjust for the last chunk

        doc_chunk = nlp.make_doc(doc[start_idx:end_idx].text)
        doc_chunk.user_data = doc.user_data.copy()
        doc_chunk.user_data["_split_id"] = split_id_counter
        split_id_counter += 1

        doc_chunks.append(doc_chunk)

        # Exit loop if this was the last possible chunk
        if end_idx == len(doc):
            break

        i += split_length - split_overlap  # Step forward, considering overlap

    return doc_chunks

def process_file(file_path: Path) -> Dict:
    """Processes a single file based on file type."""
    if file_path.suffix.lower() in ['.pdf']:
        return pdf_load_file(file_path)
    elif file_path.suffix.lower() in ['.txt', '.md', '.mdx', '.json']:
        return text_load_file(file_path)
    else:
        msg.warn(f"Unsupported file type: {file_path.suffix}")
        return {}

def process_directory(dir_path: Path) -> Dict:
    """Processes all files in a directory."""
    file_contents = {}
    for file_path in dir_path.rglob('*'):
        file_content = process_file(file_path)
        if file_content:
            file_contents[file_path.name] = file_content
    return file_contents

def convert_files(
    client: Client, files: dict, nlp: Language, doc_type: str = "Documentation"
) -> list[Doc]:
    """Converts list of strings to list of spaCy Documents."""
    raw_docs = []
    for file_name in files:
        doc = nlp(text=files[file_name])
        doc.user_data = {
            "doc_name": file_name,
            "doc_hash": hash_string(file_name),
            "doc_type": doc_type,
            "doc_link": "",
        }
        msg.info(f"Converted {doc.user_data['doc_name']}")
        if not check_if_file_exits(client, file_name):
            raw_docs.append(doc)
        else:
            msg.warn(f"{file_name} already exists in database")

    msg.good(f"All {len(raw_docs)} files successfully loaded")
    return raw_docs

def check_if_file_exits(client: Client, doc_name: str) -> bool:
    """Checks if a file exists in the database."""
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
