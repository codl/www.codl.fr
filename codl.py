from flask import Flask, render_template, Markup
import misaka
import importlib

app = Flask(__name__)
importlib.import_module('plumbing')


def render_markdown(filename, template='page.html'):
    with open(filename) as f:
        html = misaka.html(f.read())
        return render_template(template, content=Markup(html))


@app.route('/')
def index():
    return render_markdown('pages/index.md', template='index.html')


@app.route('/now')
def now():
    return render_markdown('pages/now.md')
