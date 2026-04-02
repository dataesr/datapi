from flask import Flask

from main import filter_data, read_data, write_data

app = Flask(__name__)

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