import os

from dotenv import load_dotenv
from pytidb import TiDBClient

load_dotenv()


async def get_tidb_connection():
    connection = TiDBClient.connect(
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

    return connection


async def get_shopping_table():
    pass
