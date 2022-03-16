from flask import Flask, render_template, make_response
import importlib

app = Flask(__name__)
importlib.import_module("codl.plumbing")


@app.route("/")
@app.route("/index.html")
def index():
    resp = make_response(render_template("index.html"))
    resp.add_etag()
    return resp
