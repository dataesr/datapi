from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
import json

import connectors.mongo as mongo
import connectors.s3 as s3
from utils import get_mongo_data, get_openapi_schema

description = "From data to API"
title = "datApi"
version = "0.0.0"
app = FastAPI(description=description, title=title, version=version)

try:
    with open("config.json", "r") as file:
        config = json.load(file)
except FileNotFoundError:
    print("Error: The file \"config.json\" was not found.")


@app.get("/", response_class=HTMLResponse)
def home():
    list = [
        f"<li><a href=\"./docs/{collection}\">{collection} | {config.get('collections', {}).get(collection, {}).get('connector')}</a></li>" for collection in config.get("collections", {}).keys()]
    return f"<h1>{title}</h1><ul>{''.join(list)}</ul>"


@app.get("/api/{collection}")
def api_collection(collection, limit: int = 20, skip: int = 0):
    if collection not in config.get("collections", {}).keys():
        return f"The collection \"{collection}\" does not exist", 500
    filter = config.get("collections", {}).get(collection, {}).get("filter", {})
    return get_mongo_data(collection, filter=filter, limit=limit, skip=skip)


@app.get("/docs/{collection}")
def doc_collection(collection):
    if collection not in config.get("collections", {}).keys():
        return f"The collection \"{collection}\" does not exist", 500
    return get_swagger_ui_html(openapi_url=f"/json/{collection}", title=title)


@app.get("/json/{collection}")
def json_collection(collection):
    if collection not in config.get("collections", {}).keys():
        return f"The collection \"{collection}\" does not exist.", 500
    connector = config.get("collections", {}).get(collection, {}).get("connector")
    if connector not in ["cartable", "mongo"]:
        return f"The connector \"{connector}\" does not exist, it should be one of [\"cartable\", \"mongo\"]", 500
    if connector == "mongo":
        df = mongo.get_data(collection_name=f"{collection}")
    elif connector == "cartable":
        df = s3.get_s3_data(file=f"{collection}.csv")
    paths = get_openapi_schema(collection_name=collection, df=df)
    return {
        "openapi": "3.0.0",
        "info": {
            "title": f"{title} - {collection}",
            "version": version,
            "description": f"Documentation générée automatiquement à partir d'un échantillon de 20 documents de la collection **{collection}**.",
        },
        "paths": paths,
    }
