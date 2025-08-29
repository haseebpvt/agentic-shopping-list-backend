import os

from dotenv import load_dotenv
from pytidb import TiDBClient

load_dotenv()


async def get_tidb_connection():
    tidb_client = TiDBClient.connect(
        host=os.getenv("TIDB_HOST"),
        port=int(os.getenv("TIDB_PORT")),
        user=os.getenv("TIDB_USERNAME"),
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


async def get_shopping_table():
    pass
