from mongo import close_db, get_collection


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


def get_data(collection_name, filter: dict = {}, limit: int = 20, skip: int = 0):
    try:
        collection = get_collection(collection_name)
        data = list(collection.find(
            filter, {"_id": False}, limit=limit, skip=skip))
        close_db()
        return data
    except Exception as e:
        raise Exception("The following error occurred: ", e)


def get_json_collection(collection_name):
    collection = get_collection(collection_name)
    docs = collection.find({}, {"_id": False}).limit(20)
    properties = {}
    for doc in docs:
        for key in doc.keys():
            if key not in properties:
                infered_type = infer_type(doc[key])
                if infered_type != "None":
                    properties[key] = {"type": infered_type}
    paths = {
        f"/api/{collection_name}": {
            "get": {
                "summary": f"Lister les documents de {collection_name}",
                "parameters": [
                    {"name": "limit", "in": "query", "schema": {
                        "type": "integer", "default": 20}},
                    {"name": "skip", "in": "query", "schema": {
                        "type": "integer", "default": 0}},
                    {"name": "sort", "in": "query", "schema": {
                        "type": "string"}, "description": "Ex: -annee-universitaire"},
                    *[{"name": prop, "in": "query", "schema": {"type": properties[prop]["type"]}, "description": f"Filtrer par {prop}"} for prop in properties]
                ],
                "responses": {
                    200: {
                        "description": "Liste de documents",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "total": {"type": "integer"},
                                        "data": {"type": "array", "items": {"type": "object", "properties": properties}},
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


def get_openapi_schema(collection_name, df):
    properties = {}
    for index, dtype in enumerate(df.dtypes):
        properties[df.columns[index]] = {"type": str(dtype)}
    paths = {
        f"/api/{collection_name}": {
            "get": {
                "summary": f"Lister les documents de {collection_name}",
                "parameters": [
                    {"name": "limit", "in": "query", "schema": {
                        "type": "integer", "default": 20}},
                    {"name": "skip", "in": "query", "schema": {
                        "type": "integer", "default": 0}},
                    {"name": "sort", "in": "query", "schema": {
                        "type": "string"}, "description": "Ex: -annee-universitaire"},
                    *[{"name": prop, "in": "query", "schema": {"type": properties[prop]["type"]}, "description": f"Filtrer par {prop}"} for prop in properties]
                ],
                "responses": {
                    200: {
                        "description": "Liste de documents",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "total": {"type": "integer"},
                                        "data": {"type": "array", "items": {"type": "object", "properties": properties}},
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
