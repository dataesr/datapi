from dotenv import load_dotenv
import os
import pymongo
import time

# Load environment variables from .env file
load_dotenv()

mongoDbName = os.getenv("MONGO_DB_NAME", "dataesr")
mongoUri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

def read_data():
  print("read_table")
  try:
      start = time.time()
      client = pymongo.MongoClient(mongoUri)
      database = client[mongoDbName]
      collection = database["atlas2023"]
      data = list(collection.find())
      client.close()
      end = time.time()
      print(end - start)
      return data
  except Exception as e:
      raise Exception("The following error occurred: ", e)

def filter_data(data):
  print("filter_data")
  start = time.time()
  res = [d for d in data if d.get("secret") != 'oui']
  end = time.time()
  print(end - start)
  return res

def write_data(data):
  print("write_data")
  start = time.time()
  client = pymongo.MongoClient(mongoUri)
  database = client[mongoDbName]
  collection = database["atlas2023-anne"]
  # TODO: use bulk_insert instead of insert_many
  collection.insert_many(data)
  end = time.time()
  print(end - start)

data = read_data()
print(len(data))
filtered_data = filter_data(data)
print(len(filtered_data))
write_data(filtered_data)
print("done")
