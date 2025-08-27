import os

import pymysql
from dotenv import load_dotenv

load_dotenv()


async def get_tidb_connection():
    connection = pymysql.connect(
        host=os.getenv("TIDB_HOST"),
        port=int(os.getenv("TIDB_PORT")),
        user=os.getenv("TIDB_USERNAME"),
        password=os.getenv("TIDB_PASSWORD"),
        database=os.getenv("TIDB_DATABASE"),
        # ssl_verify_cert=True,
        # ssl_verify_identity=True,
        # ssl_ca="/etc/ssl/cert.pem"
    )

    return connection

# async def get_shopping_table():

