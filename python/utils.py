from mongo import close_db, get_collection

def read_data(collection_name):
  try:
    collection = get_collection(collection_name)
    data = list(collection.find())
    close_db()
    return data
  except Exception as e:
    raise Exception("The following error occurred: ", e)

def filter_data(data):
  return [d for d in data if d.get("secret") == "non"]

def write_data(collection_name, data):
  collection = get_collection(f"{collection_name}-tmp")
  # TODO: use bulk_insert instead of insert_many
  collection.insert_many(data)
  close_db()

def infer_type(obj):
  openapi_types = {
    "bool": "boolean",
    "datetime": "string",
    "dict": "object",
    "float": "number",
    "int": "integer",
    "list": "array",
    "NoneType": "None",
    "str": "string"
  }
  object_type = type(obj).__name__
  openapi_type = openapi_types[object_type] if object_type in openapi_types else "unknown"
  if openapi_type == "unknown":
    print(f"Error: {object_type} is unknown.")
  return openapi_type

def get_collection_doc(collection_name):
  collection = get_collection(collection_name)
  docs = collection.find({}).limit(20)
  properties = {}
  for doc in docs:
    keys = [t for t in doc.keys() if t not in ['_id']]
    for key in keys:
      if key not in properties:
        infered_type = infer_type(doc[key])
        if infered_type != 'None':
          properties[key] = infered_type
  paths = {
    f"/api/{collection_name}": {
      "get": {
          "summary": "Lister les documents de ${collection}",
          "parameters": [
            { "name": "limit", "in": "query", "schema": { "type": "integer", "default": 20 } },
            { "name": "skip", "in": "query", "schema": { "type": "integer", "default": 0 } },
            { "name": "sort", "in": "query", "schema": { "type": "string" }, "description": "Ex: -annee-universitaire" },
            [{ "name": prop, "in": "query", "schema": { "type": properties[prop] }, "description": f"Filtrer par {prop}" } for prop in properties]
          ],
          "responses": {
            200: {
              "description": "Liste de documents",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "total": { "type": "integer" },
                      "data": { "type": "array", "items": { "type": "object", "properties": properties } },
                    },
                  },
                },
              },
            },
          },
        },
    }
  }
  return paths