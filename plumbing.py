"""
legacy redirects and hacky routing
"""

from codl import app
from flask import redirect, url_for

@app.route('/herd.html')
def redir_herd():
    return redirect(url_for('index'), code=301)

@app.route('/.well-known/keybase.txt', defaults={'filename': 'keybase.txt'})
@app.route('/robots.txt', defaults={'filename': 'robots.txt'})
@app.route('/humans.txt', defaults={'filename': 'humans.txt'})
def route_to_static(filename):
    return app.view_functions['static'](filename=filename)
