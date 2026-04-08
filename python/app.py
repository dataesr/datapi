import json
from flask import Flask
from swagger_ui import api_doc

from utils import get_collection_doc, filter_data, read_data, write_data

app = Flask(__name__)

try:
    with open("config.json", "r") as file:
        config = json.load(file)
except FileNotFoundError:
    print("Error: The file \"config.json\" was not found.")

# TODO Display documentation for all collections ie. create a config file to list all collections
doc = get_collection_doc(config["collections"][0])
api_doc(app, config=doc, url_prefix='/doc', title='API doc')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/read")
def read():
    data = read_data(config["collections"][0])
    print(len(data))
    filtered_data = filter_data(data)
    print(len(filtered_data))
    write_data(config["collections"][0], filtered_data)
    print("done")
    return "<p>Job done</p>"

@app.route("/api/doc/<collection>")
def doc_collection(collection):
    if collection not in config["collections"]:
        return f"The collection \"{collection}\" does not exist", 500
    doc = get_collection_doc(collection)
    return doc, 200