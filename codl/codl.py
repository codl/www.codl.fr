from flask import Flask, render_template, Markup, render_template_string
import misaka
import importlib
from pathlib import Path

app = Flask(__name__)
importlib.import_module('codl.plumbing')


def render_markdown(filename, template='page.html'):
    filename = str(Path(app.root_path) / filename)
    with open(filename) as f:
        markdown = f.read()
        processed = render_template_string(markdown)

        html = misaka.html(processed)
        return render_template(template, content=Markup(html))


@app.route('/')
def index():
    return render_markdown('pages/index.md', template='index.html')


@app.route('/now')
def now():
    return render_markdown('pages/now.md')


@app.route('/contact')
def contact():
    return render_markdown('pages/contact.md')
