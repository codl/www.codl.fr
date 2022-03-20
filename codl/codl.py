"""
Main pages go here
"""
from flask import Flask, render_template, make_response
import importlib

app = Flask(__name__)
importlib.import_module("codl.plumbing")


@app.route("/index.html")
@app.route("/")
def index():
    "Serves the index page."
    resp = make_response(render_template("index.html"))
    resp.add_etag()
    return resp
