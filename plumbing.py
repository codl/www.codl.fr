"""
legacy redirects and hacky routing
"""

from codl import app
from flask import redirect, url_for, abort
import os
import yaml
import random

@app.route('/herd.html')
def redir_herd():
    return redirect(url_for('index'), code=301)

@app.route('/.well-known/keybase.txt', defaults={'filename': 'keybase.txt'})
@app.route('/robots.txt', defaults={'filename': 'robots.txt'})
@app.route('/humans.txt', defaults={'filename': 'humans.txt'})
def route_to_static(filename):
    return app.view_functions['static'](filename=filename)

@app.route('/static-<int:timestamp>/<path:filename>')
def static_cachebust(timestamp, filename):
    path = os.path.join(app.static_folder, filename)
    mtime = os.stat(path).st_mtime
    if abs(mtime - timestamp) > 1:
        abort(404)
    else:
        resp = route_to_static(filename)
        resp.headers.set('cache-control', 'public, immutable, max-age=%s' % (60*60*24*365,))
        if 'expires' in resp.headers:
            resp.headers.remove('expires')
        return resp

@app.context_processor
def replace_url_for():
    return dict(url_for = cachebust_url_for)

def cachebust_url_for(endpoint, **kwargs):
    if endpoint == 'static':
        endpoint = 'static_cachebust'
        path = os.path.join(app.static_folder, kwargs.get('filename'))
        kwargs['timestamp'] = int(os.stat(path).st_mtime)
    return url_for(endpoint, **kwargs)
