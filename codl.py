from flask import Flask
from lib.markdown import render_markdown

app = Flask(__name__)


@app.route('/')
def index():
    return render_markdown('index.md')


@app.route('/enby')
def enby():
    return render_markdown('enby.md', title='non-binary')


import plumbing
