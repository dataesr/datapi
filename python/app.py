from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
import json

from utils import get_collection_doc

app = FastAPI(
    title="datApi",
    description="From data to API",
    version="0.0.0"
)

try:
    with open("config.json", "r") as file:
        config = json.load(file)
except FileNotFoundError:
    print("Error: The file \"config.json\" was not found.")


@app.get("/", response_class=HTMLResponse)
def home():
    list = [
        f"<li><a href=\"./docs/{collection}\">{collection}</a></li>" for collection in config["collections"]]
    return f"<h1>datApi</h1><ul>{''.join(list)}</ul>"


# @app.get("/read")
# def read():
#     data = read_data(config["collections"][0])
#     filtered_data = filter_data(data)
#     write_data(config["collections"][0], filtered_data)
#     return "<p>Job done</p>"


@app.get("/json/{collection}")
def json_collection(collection):
    if collection not in config["collections"]:
        return f"The collection \"{collection}\" does not exist", 500
    paths = get_collection_doc(collection)
    return {
        "openapi": "3.0.0",
        "info": {
            "title": f"datapi - {collection}",
            "version": "1.0.0",
            "description": f"Documentation générée automatiquement à partir d'un échantillon de 20 documents de la collection **{collection}**.",
        },
        "paths": paths,
    }


@app.get("/docs/{collection}")
def swagger_collection(collection):
    if collection not in config["collections"]:
        return f"The collection \"{collection}\" does not exist", 500
    return get_swagger_ui_html(openapi_url=f"/json/{collection}", title="datApi")
