import os
from pathlib import Path
from wasabi import msg
import spacy
from app.common.util import vector_client, import_documents, import_chunks
from app.controllers.reader.ProcessingHub import process_file, process_directory, chunk_docs, convert_files
from app.controllers.schema.init_schema import init_schema
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def ImportData(path_str: str, model: str) -> None:
    """
    Import and process data.

    Parameters:
    path_str (str): Path to the data file or directory.
    model (str): Name of the model to use.

    Returns:
    None
    """
    data_path = Path(path_str)
    msg.divider("Starting data import")
    
    # Initialize NLP model
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")

    # Set up client
    client = vector_client()
    if not client:
        msg.fail("Client setup failed")
        return

    # Initialize database schema
    if not client.schema.exists("Document"):
        init_schema(model)
    msg.info("All schemas available")

    # Process file or directory
    file_contents = {}
    if data_path.is_file():
        file_contents = process_file(data_path)
    else:
        file_contents = process_directory(data_path)

    # Import documents and data chunks
    if file_contents:
        documents = convert_files(client, file_contents, nlp=nlp)
        if documents:
            chunks = chunk_docs(documents, nlp)
            uuid_map = import_documents(client=client, documents=documents)
            import_chunks(client=client, chunks=chunks, doc_uuid_map=uuid_map)

    # Stop the embedded database
    if client._connection.embedded_db:
        msg.info("Stopping Weaviate Embedded")
        client._connection.embedded_db.stop()
