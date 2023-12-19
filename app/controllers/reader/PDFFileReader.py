import glob
import os
from spacy.tokens import Doc
from spacy.language import Language
from pathlib import Path
from wasabi import msg

try:
    from PyPDF2 import PdfReader
except Exception:
    msg.warn("PyPDF2 not installed")

def pdf_load_file(file_path: Path) -> dict:
    """
    Load a PDF file and return its contents in a dictionary.
    Parameters:
        file_path : Path - The path to the file.
    Returns:
        dict - A dictionary containing the filename (key) and content (value).
    """
    file_contents = {}
    file_types = [".pdf"]

    # Check if the file type is supported
    if file_path.suffix.lower() not in file_types:
        print(f"{file_path.suffix} not supported.")
        return {}

    # Initialize a variable to hold the entire text of the PDF
    full_text = ""
    
    # Read the PDF file
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:  # Check if text extraction was successful
                full_text += text + "\n\n"
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return {}

    # Store the extracted text in a dictionary
    file_contents[file_path.name] = full_text.strip()

    print(f"File loaded: {file_path.name}")

    return file_contents
