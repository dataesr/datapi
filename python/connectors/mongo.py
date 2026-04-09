from dotenv import load_dotenv
import os
import pandas as pd
import pymongo
from retry import retry
from typing import Union

# Load environment variables from .env file
load_dotenv()

mongo_db_name = os.getenv("MONGO_DB_NAME", "dataesr")
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = None


def get_client() -> Union[pymongo.MongoClient, None]:
  global client
  if client is None:
    client = pymongo.MongoClient(mongo_uri, connectTimeoutMS=60000)
  return client


def get_database(database: str = mongo_db_name) -> Union[pymongo.database.Database, None]:
  _client = get_client()
  db = _client[database]
  return db


@retry(delay=200, tries=2)
def get_collection(collection_name: str) -> Union[pymongo.collection.Collection, None]:
  db = get_database()
  collection = db[collection_name]
  return collection


def close_db():
  global client
  client.close()
  client = None


def get_data(collection_name):
    try:
        collection = get_collection(collection_name)
        docs = collection.find({}, {"_id": False}).limit(20)
        return pd.DataFrame(list(docs))
    except Exception as error:
        raise Exception("The following error occurred: ", error)