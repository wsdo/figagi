import hashlib
import ssl
import os

import openai
import weaviate
from weaviate import Client
from typing import Optional
from spacy.tokens import Doc

from weaviate.embedded import EmbeddedOptions

from wasabi import msg


def setup_client() -> Optional[Client]:
    """
    @returns Optional[Client] - The Weaviate Client
    """

    msg.info("Setting up client")

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    weaviate_url = os.environ.get("VERBA_URL", "")
    weaviate_key = os.environ.get("VERBA_API_KEY", "")

    if openai_key == "":
        msg.fail("OPENAI_API_KEY environment variable not set")
        return None

    # Weaviate Embedded
    elif weaviate_url == "":
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        msg.info("VERBA_URL environment variable not set. Using Weaviate Embedded")
        client = weaviate.Client(
            additional_headers={"X-OpenAI-Api-Key": openai.api_key},
            embedded_options=EmbeddedOptions(
                persistence_data_path="./.verba/local/share/",
                binary_path="./.verba/cache/weaviate-embedded",
            ),
        )
        msg.good("Client connected to local Weaviate server")
        return client

    elif weaviate_key == "":
        msg.warn("VERBA_API_KEY environment variable not set")

    openai.api_key = openai_key
    url = weaviate_url
    auth_config = weaviate.AuthApiKey(api_key=weaviate_key)

    client = weaviate.Client(
        url=url,
        additional_headers={"X-OpenAI-Api-Key": openai.api_key},
        auth_client_secret=auth_config,
    )

    msg.good("Client connected to Weaviate Cluster")

    return client


def hash_string(text: str) -> str:
    """Hash a string
    @parameter text : str - The string to hash
    @returns str - Hashed string
    """
    # Create a new sha256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the bytes-like object (filepath)
    sha256.update(text.encode())

    # Return the hexadecimal representation of the hash
    return str(sha256.hexdigest())


def import_documents(client: Client, documents: list[Doc]) -> dict:
    """Imports a list of document to the Weaviate Client and returns a list of UUID for the chunks to match
    @parameter client : Client - Weaviate Client
    @parameter documents : list[Document] - List of whole documents
    @returns dict - The UUID list
    """
    doc_uuid_map = {}

    with client.batch as batch:
        batch.batch_size = 100
        for i, d in enumerate(documents):
            msg.info(
                f"({i+1}/{len(documents)}) Importing document {d.user_data['doc_name']}"
            )

            properties = {
                "text": str(d.text),
                "doc_name": str(d.user_data["doc_name"]),
                "doc_type": str(d.user_data["doc_type"]),
                "doc_link": str(d.user_data["doc_link"]),
            }

            uuid = client.batch.add_data_object(properties, "Document")
            uuid_key = str(d.user_data["doc_hash"]).strip().lower()
            doc_uuid_map[uuid_key] = uuid

    msg.good("Imported all docs")
    return doc_uuid_map


def import_chunks(client: Client, chunks: list[Doc], doc_uuid_map: dict) -> None:
    """Imports a list of chunks to the Weaviate Client and uses a list of UUID for the chunks to match
    @parameter client : Client - Weaviate Client
    @parameter chunks : list[Document] - List of chunks of documents
    @parameter doc_uuid_map : dict  UUID list of documents the chunks belong to
    @returns None
    """
    with client.batch as batch:
        batch.batch_size = 100
        for i, d in enumerate(chunks):
            msg.info(
                f"({i+1}/{len(chunks)}) Importing chunk of {d.user_data['doc_name']} ({d.user_data['_split_id']})"
            )

            uuid_key = str(d.user_data["doc_hash"]).strip().lower()
            uuid = doc_uuid_map[uuid_key]

            properties = {
                "text": str(d.text),
                "doc_name": str(d.user_data["doc_name"]),
                "doc_uuid": uuid,
                "doc_type": str(d.user_data["doc_type"]),
                "chunk_id": int(d.user_data["_split_id"]),
            }

            client.batch.add_data_object(properties, "Chunk")

    msg.good("Imported all chunks")
