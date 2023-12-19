import glob
from pathlib import Path
from wasabi import msg

def text_load_file(file_path: Path) -> dict:
    """
    Read a text file.

    @param file_path : Path - The path to the file
    @return dict - Returns a dictionary containing the file name (key) and its content (value)
    """
    file_contents = {}
    supported_file_types = [".txt", ".md", ".mdx", ".json"]

    if file_path.suffix.lower() not in supported_file_types:
        msg.warn(f"Unsupported file type: {file_path.suffix}")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            msg.info(f"Reading {str(file_path)}")
            file_contents[str(file_path)] = f.read()
        msg.good(f"Loaded {len(file_contents)} files")
    except IOError as e:
        msg.fail(f"Error reading file {str(file_path)}: {e}")

    return file_contents
