from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
import json

from utils import get_data, get_json_collection

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
        f"<li><a href=\"./docs/{collection}\">{collection}</a></li>" for collection in config["collections"]]
    return f"<h1>{title}</h1><ul>{''.join(list)}</ul>"


@app.get("/api/{collection}")
def api_collection(collection, limit: int = 20, skip: int = 0):
    if collection not in config["collections"]:
        return f"The collection \"{collection}\" does not exist", 500
    return get_data(collection, limit=limit, skip=skip)


@app.get("/docs/{collection}")
def doc_collection(collection):
    if collection not in config["collections"]:
        return f"The collection \"{collection}\" does not exist", 500
    return get_swagger_ui_html(openapi_url=f"/json/{collection}", title=title)


@app.get("/json/{collection}")
def json_collection(collection):
    if collection not in config["collections"]:
        return f"The collection \"{collection}\" does not exist", 500
    paths = get_json_collection(collection)
    return {
        "openapi": "3.0.0",
        "info": {
            "title": f"{title} - {collection}",
            "version": version,
            "description": f"Documentation générée automatiquement à partir d'un échantillon de 20 documents de la collection **{collection}**.",
        },
        "paths": paths,
    }