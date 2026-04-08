from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
from swagger_ui import api_doc

from utils import get_collection_doc, filter_data, read_data, write_data

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

paths = [get_collection_doc(collection_name) for collection_name in config["collections"]]
merged = dict()
for path in paths:
    merged.update(path)
doc = {
    "openapi": "3.0.0",
    "info": {
        "title": "datapi",
        "version": "1.0.0",
        "description": f"Documentation générée automatiquement à partir d'un échantillon de 20 documents des collections **{', '.join(config['collections'])}**.",
    },
    "paths": merged,
}
api_doc(app, config=doc, url_prefix="/doc", title="API doc")

@app.get("/", response_class=HTMLResponse)
def home():
    # TODO: Replace it by a list of available collections , and link to the dedicated page
    # return "<p>Hello, World!</p>"
    list = [f"<li><a href=\"./api/doc/{collection}\">{collection}</a></li>" for collection in config["collections"]]
    return f"<h1>datApi</h1><ul>{''.join(list)}</ul>"

@app.get("/read")
def read():
    data = read_data(config["collections"][0])
    filtered_data = filter_data(data)
    write_data(config["collections"][0], filtered_data)
    return "<p>Job done</p>"

@app.get("/api/doc/{collection}")
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
    }, 200

@app.get("/doc/{collection}")
def swagger_collection(collection):
    if collection not in config["collections"]:
        return f"The collection \"{collection}\" does not exist", 500
    paths = get_collection_doc(collection)
    doc = {
        "openapi": "3.0.0",
        "info": {
        "title": f"datapi - {collection}",
        "version": "1.0.0",
        "description": f"Documentation générée automatiquement à partir d'un échantillon de 20 documents de la collection **{collection}**.",
        },
        "paths": paths,
    }
    api_doc(app, config=doc, url_prefix=f"/doc/{collection}", title="API doc")
