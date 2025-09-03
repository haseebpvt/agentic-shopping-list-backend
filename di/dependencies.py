import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from langgraph.checkpoint.memory import InMemorySaver
from pytidb import TiDBClient, Table

from db.model.shopping_item import PreferenceTable

load_dotenv()


def get_tidb_connection():
    tidb_client = TiDBClient.connect(
        host=os.getenv("TIDB_HOST"),
        port=int(os.getenv("TIDB_PORT")),
        username=os.getenv("TIDB_USERNAME"),
        password=os.getenv("TIDB_PASSWORD"),
        database=os.getenv("TIDB_DATABASE"),
        ensure_db=True,
        # ssl_verify_cert=True,
        # ssl_verify_identity=True,
        # ssl_ca="/etc/ssl/cert.pem"
    )

    # Add text embedding support
    tidb_client.configure_embedding_provider(
        "openai",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    return tidb_client


def get_shopping_table(tidb_client: Annotated[TiDBClient, Depends(get_tidb_connection)]) -> Table:
    return tidb_client.create_table(schema=PreferenceTable, if_exists="skip")


in_memory_saver = InMemorySaver()


def get_checkpoint_saver():
    return in_memory_saver
