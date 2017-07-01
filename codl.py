from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/services/')
def services():
    return render_template('services.html')

import plumbing
