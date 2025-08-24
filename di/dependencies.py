import os

import pymysql
from dotenv import load_dotenv

load_dotenv()


async def get_tidb_connection():
    connection = pymysql.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user=os.getenv("TIDB_USER"),
        password=os.getenv("TIDB_PASSWORD"),
        database="shopping",
        ssl_verify_cert=True,
        ssl_verify_identity=True,
        ssl_ca="/etc/ssl/cert.pem"
    )

    return connection
