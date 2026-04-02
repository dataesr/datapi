import time

from mongo import close_db, get_collection

def read_data():
  print("read_table")
  try:
    start = time.time()
    collection = get_collection("atlas2023")
    data = list(collection.find())
    close_db()
    end = time.time()
    print(end - start)
    return data
  except Exception as e:
    raise Exception("The following error occurred: ", e)

def filter_data(data):
  print("filter_data")
  start = time.time()
  res = [d for d in data if d.get("secret") == "non"]
  end = time.time()
  print(end - start)
  return res

def write_data(data):
  print("write_data")
  start = time.time()
  collection = get_collection("atlas2023-anne")
  # TODO: use bulk_insert instead of insert_many
  collection.insert_many(data)
  close_db()
  end = time.time()
  print(end - start)
