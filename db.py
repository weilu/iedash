from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os


SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
HTTP_PATH = os.getenv("HTTP_PATH")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

CORP_CATALOG = "prd_corpdata"
CORP_SCHEMA = "dm_operation_gold"

def get_db_url(catalog, schema):
    return URL.create(
        "databricks",
        username="token",
        password=ACCESS_TOKEN,
        host=SERVER_HOSTNAME,
        query={
            "http_path": HTTP_PATH,
            "catalog": CORP_CATALOG,
            "schema": CORP_SCHEMA,
        }
    )

corp_engine = create_engine(get_db_url(CORP_CATALOG, CORP_SCHEMA), echo=True)

