from flask import Flask, render_template, Markup
import misaka
import importlib

app = Flask(__name__)


@app.route('/')
def index():
    with open('pages/index.md') as f:
        html = misaka.html(f.read())
        return render_template('index.html', content=Markup(html))


importlib.import_module('plumbing')
