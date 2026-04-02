from dotenv import load_dotenv
import os
import pymongo
from retry import retry
from typing import Union

# Load environment variables from .env file
load_dotenv()

mongoDbName = os.getenv("MONGO_DB_NAME", "dataesr")
mongoUri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = None


def get_client() -> Union[pymongo.MongoClient, None]:
  global client
  if client is None:
    client = pymongo.MongoClient(mongoUri, connectTimeoutMS=60000)
  return client


def get_database(database: str = mongoDbName) -> Union[pymongo.database.Database, None]:
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
