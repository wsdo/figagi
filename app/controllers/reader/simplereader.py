import base64
import glob
import json
from datetime import datetime
from pathlib import Path

from wasabi import msg

from goldenverba.components.reader.document import Document
from goldenverba.components.reader.interface import InputForm, Reader


class SimpleReader(Reader):
    """
    The SimpleReader reads .txt, .md, .mdx, and .json files. It can handle both paths, content and bytes.
    """

    def __init__(self):
        super().__init__()
        self.file_types = [".txt", ".md", ".mdx", ".json"]
        self.name = "SimpleReader"
        self.description = "Reads text, markdown, and json files."
        self.input_form = InputForm.UPLOAD.value

    def load(
        self,
        bytes: list[str] = None,
        contents: list[str] = None,
        paths: list[str] = None,
        fileNames: list[str] = None,
        document_type: str = "Documentation",
    ) -> list[Document]:
        """Ingest data into Weaviate
        @parameter: bytes : list[str] - List of bytes
        @parameter: contents : list[str] - List of string content
        @parameter: paths : list[str] - List of paths to files
        @parameter: fileNames : list[str] - List of file names
        @parameter: document_type : str - Document type
        @returns list[Document] - Lists of documents.
        """
        if fileNames is None:
            fileNames = []
        if paths is None:
            paths = []
        if contents is None:
            contents = []
        if bytes is None:
            bytes = []
        documents = []

        # If paths exist
        if len(paths) > 0:
            for path in paths:
                if path != "":
                    data_path = Path(path)
                    if data_path.exists():
                        if data_path.is_file():
                            documents += self.load_file(data_path, document_type)
                        else:
                            documents += self.load_directory(data_path, document_type)
                    else:
                        msg.warn(f"Path {data_path} does not exist")

        # If bytes exist
        if len(bytes) > 0 and len(bytes) == len(fileNames):
            for byte, fileName in zip(bytes, fileNames):
                decoded_bytes = base64.b64decode(byte)
                try:
                    original_text = decoded_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    msg.fail(
                        f"Error decoding text for file {fileName}. The file might not be a text file."
                    )
                    continue

                if ".json" in fileName:
                    json_obj = json.loads(original_text)
                    try:
                        document = Document.from_json(json_obj)
                    except Exception as e:
                        raise Exception(f"Loading JSON failed {e}")

                else:
                    document = Document(
                        name=fileName,
                        text=original_text,
                        type=document_type,
                        timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        reader=self.name,
                    )
                documents.append(document)

        # If content exist
        if len(contents) > 0 and len(contents) == len(fileNames):
            for content, fileName in zip(contents, fileNames):
                document = Document(
                    name=fileName,
                    text=content,
                    type=document_type,
                    timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    reader=self.name,
                )
                documents.append(document)

        msg.good(f"Loaded {len(documents)} documents")
        return documents

    def load_file(self, file_path: Path, document_type: str) -> list[Document]:
        """Loads text file
        @param file_path : Path - Path to file
        @param document_type : str - Document Type
        @returns list[Document] - Lists of documents.
        """
        documents = []

        if file_path.suffix not in self.file_types:
            msg.warn(f"{file_path.suffix} not supported")
            return []

        with open(file_path, encoding="utf-8") as f:
            msg.info(f"Reading {str(file_path)}")

            if file_path.suffix == ".json":
                json_obj = json.loads(f.read())
                try:
                    document = Document.from_json(json_obj)
                except Exception as e:
                    raise Exception(f"Loading JSON failed {e}")

            else:
                document = Document(
                    text=f.read(),
                    type=document_type,
                    name=str(file_path),
                    link=str(file_path),
                    timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    reader=self.name,
                )
            documents.append(document)
        msg.good(f"Loaded {str(file_path)}")
        return documents

    def load_directory(self, dir_path: Path, document_type: str) -> list[Document]:
        """Loads text files from a directory and its subdirectories.

        @param dir_path : Path - Path to directory
        @param document_type : str - Document Type
        @returns list[Document] - List of documents
        """
        # Initialize an empty dictionary to store the file contents
        documents = []

        # Convert dir_path to string, in case it's a Path object
        dir_path_str = str(dir_path)

        # Loop through each file type
        for file_type in self.file_types:
            # Use glob to find all the files in dir_path and its subdirectories matching the current file_type
            files = glob.glob(f"{dir_path_str}/**/*{file_type}", recursive=True)

            # Loop through each file
            for file in files:
                msg.info(f"Reading {str(file)}")
                with open(file, encoding="utf-8") as f:
                    document = Document(
                        text=f.read(),
                        type=document_type,
                        name=str(file),
                        link=str(file),
                        timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        reader=self.name,
                    )

                    documents.append(document)

        msg.good(f"Loaded {len(documents)} documents")
        return documents
