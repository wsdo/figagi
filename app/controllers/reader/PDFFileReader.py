import glob
import os
import json

from app.common.util import hash_string
from spacy.tokens import Doc
from spacy.language import Language
from weaviate import Client
from pathlib import Path
from wasabi import msg  # type: ignore[import]

try:
    from PyPDF2 import PdfReader
except Exception:
    msg.warn("PyPDF2 not installed, your base installation might be corrupted.")

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


# Loading Files from Directory


from pathlib import Path
from PyPDF2 import PdfReader

def pdf_load_file(file_path: Path) -> dict:
    """Loads a PDF file and returns its contents in a dictionary.
    @param file_path : Path - Path to the file
    @returns dict - Dictionary of filename (key) and their content (value)
    """
    file_contents = {}
    file_types = [".pdf"]

    # Check if the file type is supported
    if file_path.suffix.lower() not in file_types:
        print(f"{file_path.suffix} not supported.")
        return {}

    # Initialize a variable to hold the full text of the PDF
    full_text = ""
    
    # Read the PDF file
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:  # Check if text was successfully extracted
                full_text += text + "\n\n"
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return {}

    # Store the extracted text in the dictionary
    file_contents[file_path.name] = full_text.strip()

    print(f"Loaded file: {file_path.name}")

    return file_contents



def pdf_load_directory(dir_path: Path) -> dict:
    """Loads text files from a directory and its subdirectories.

    @param dir_path : Path - Path to directory
    @returns dict - Dictionary of filename (key) and their content (value)
    """
    # Initialize an empty dictionary to store the file contents
    file_contents = {}

    # Convert dir_path to string, in case it's a Path object
    dir_path_str = str(dir_path)

    # Create a list of file types you want to read
    file_types = ["pdf", "md", "mdx","json"]

    # Loop through each file type
    for file_type in file_types:
        # Use glob to find all the files in dir_path and its subdirectories matching the current file_type
        files = glob.glob(f"{dir_path_str}/**/*.{file_type}", recursive=True)

        # Loop through each file
        for file in files:
            msg.info(f"Reading {str(file)}")
            with open(file, "r", encoding="utf-8") as f:
                # Read the file and add its content to the dictionary
                file_contents[str(file)] = f.read()

    msg.good(f"Loaded {len(file_contents)} files")
    return file_contents
