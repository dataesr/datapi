from flask import Flask
from swagger_ui import api_doc

from utils import get_collection_doc, filter_data, read_data, write_data

app = Flask(__name__)

# TODO Display documentation for all collections ie. create a config file to list all collections
config = get_collection_doc("atlas2023")
api_doc(app, config=config, url_prefix='/doc', title='API doc')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/read")
def read():
    data = read_data()
    print(len(data))
    filtered_data = filter_data(data)
    print(len(filtered_data))
    write_data(filtered_data)
    print("done")
    return "<p>Job done</p>"

# TODO: Catch if collection does not exist in config file
@app.route("/api/doc/<collection>")
def doc_collection(collection):
    config = get_collection_doc(collection)
    return config