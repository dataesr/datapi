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
