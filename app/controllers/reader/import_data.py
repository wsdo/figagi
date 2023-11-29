import os
from pathlib import Path
from wasabi import msg
import spacy

from app.common.util import (
    setup_client,
    import_documents,
    import_chunks,
)
from app.controllers.reader.preprocess import (
    load_directory,
    convert_files,
    chunk_docs,
    load_file,
)

from app.controllers.schema.init_schema import init_schema
from dotenv import load_dotenv

load_dotenv()


def import_data(path_str: str, model: str):
    data_path = Path(path_str)
    msg.divider("Starting data import")
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")
    client = setup_client()

    if not client:
        msg.fail("Client setup failed")
        return

    if not client.schema.exists("Document"):
        init_schema(model)

    msg.info("All schemas available")

    file_contents = {}

    if data_path.is_file():
        file_contents = load_file(data_path)
    else:
        file_contents = load_directory(data_path)

    if file_contents:
        documents = convert_files(client, file_contents, nlp=nlp)
        if documents:
            chunks = chunk_docs(documents, nlp)
            uuid_map = import_documents(client=client, documents=documents)
            import_chunks(client=client, chunks=chunks, doc_uuid_map=uuid_map)

    if client._connection.embedded_db:
        msg.info("Stopping Weaviate Embedded")
        client._connection.embedded_db.stop()