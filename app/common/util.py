import hashlib
import ssl
import os
import time
import openai
import weaviate
from weaviate import Client
from typing import Optional
from spacy.tokens import Doc
from weaviate.embedded import EmbeddedOptions

from wasabi import msg
from dotenv import load_dotenv
load_dotenv()

def vector_client() -> Optional[Client]:
    """
    Set up Weaviate client.

    @returns Optional[Client] - Returns an instance of Weaviate client
    """
    msg.info("Setting up client")

    openai_key = os.getenv('OPENAI_API_KEY')
    weaviate_url = os.environ.get("WEAVIATE_URL", "")
    weaviate_key = os.environ.get("WEAVIATE_API_KEY", "")

    if openai_key == "":
        msg.fail("OPENAI_API_KEY environment variable not set")
        return None

    elif weaviate_url == "":
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        msg.info("WEAVIATE_URL environment variable not set, using Weaviate Embedded")
        client = weaviate.Client(
            additional_headers={"X-OpenAI-Api-Key": openai.api_key},
            embedded_options=EmbeddedOptions(
                persistence_data_path="./.figagi/local/share/",
                binary_path="./.figagi/cache/weaviate-embedded",
            ),
        )
        msg.good("Client connected to local Weaviate server")
        return client

    elif weaviate_key == "":
        msg.warn("WEAVIATE_API_KEY environment variable not set")

    openai.api_key = openai_key
    url = weaviate_url
    auth_config = weaviate.AuthApiKey(api_key=weaviate_key)

    client = weaviate.Client(
        url=url,
        additional_headers={"X-OpenAI-Api-Key": openai.api_key},
        auth_client_secret=auth_config,
    )

    msg.good("Client connected to Weaviate cluster")

    return client


def hash_string(text: str) -> str:
    """
    Hash a string.

    @parameter text : str - The string to hash
    @returns str - The hashed string
    """
    sha256 = hashlib.sha256()
    sha256.update(text.encode())
    return str(sha256.hexdigest())


def import_documents(client: Client, documents: list[Doc]) -> dict:
    """
    Import a list of documents into Weaviate client, and return a list of UUIDs for chunk matching.

    @parameter client : Client - Weaviate client
    @parameter documents : list[Document] - List of complete documents
    @returns dict - Returns a list of UUIDs
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
            time.sleep(0.6)  # Add delay, 600 milliseconds per loop

    msg.good("All documents imported")
    return doc_uuid_map


def import_chunks(client: Client, chunks: list[Doc], doc_uuid_map: dict) -> None:
    """
    Import a list of document chunks into Weaviate client, using the list of UUIDs for document matching.

    @parameter client : Client - Weaviate client
    @parameter chunks : list[Document] - List of document chunks
    @parameter doc_uuid_map : dict - List of UUIDs for the documents the chunks belong to
    @returns None
    """
    with client.batch as batch:
        batch.batch_size = 100
        for i, d in enumerate(chunks):
            msg.info(
                f"({i+1}/{len(chunks)}) Importing chunk of {d.user_data['doc_name']} ({d.user_data['_split_id']})"
            )

            uuid_key = str(d.user_data["doc_hash"]).strip().lower()
