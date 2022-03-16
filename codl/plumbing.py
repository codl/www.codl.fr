"""
Legacy redirects and hacky routing
"""

from .codl import app
from flask import redirect, url_for, abort, request, send_from_directory, Response
import os


@app.route("/.well-known/keybase.txt", defaults={"filename": "keybase.txt"})
@app.route("/robots.txt", defaults={"filename": "robots.txt"})
@app.route("/humans.txt", defaults={"filename": "humans.txt"})
@app.route("/ssh", defaults={"filename": "authorized_keys", "mimetype": "text/plain"})
@app.route(
    "/pgp",
    defaults={
        "filename": "codl.asc",
        "mimetype": "application/pgp-keys",
        "as_attachment": True,
    },
)
def send_from_static(filename, **kwargs):
    """
    Serves files from the static folder.
    """
    return send_from_directory(app.static_folder, filename, **kwargs)


@app.route("/_/<int:timestamp>/<path:filename>")
def static_cachebust(timestamp, filename):
    """
    Cachebusted static file serving

    Expects a timestamp in the url matching the file's mtime, serves files with
    immutable 1-year cache
    """
    path = os.path.join(app.static_folder, filename)
    mtime = os.stat(path).st_mtime
    if abs(mtime - timestamp) > 1:
        abort(404)
    else:
        resp = send_from_static(filename)
        resp.headers.set(
            "cache-control", "public, immutable, max-age=%s" % (60 * 60 * 24 * 365,)
        )
        if "expires" in resp.headers:
            resp.headers.remove("expires")
        return resp


def cachebust_url_for(endpoint, **kwargs):
    """
    Patched version of url_for that cachebusts static urls
    """
    if endpoint == "static":
        endpoint = "static_cachebust"
        path = os.path.join(app.static_folder, kwargs.get("filename"))
        kwargs["timestamp"] = int(os.stat(path).st_mtime)
    return url_for(endpoint, **kwargs)


@app.context_processor
def replace_url_for():
    """
    Context processor that patches in the version of url_for with cachebusted static files
    """
    return dict(url_for=cachebust_url_for)


@app.route("/.well-known/webfinger")
def webfinger():
    """
    Redirects webfinger requests for codl@codl.fr to codl@chitter.xyz
    """
    resource = request.args["resource"]
    if resource == "acct:codl@codl.fr":
        return redirect(
            "https://chitter.xyz/.well-known/webfinger?resource=acct%3Acodl%40chitter.xyz"
        )
        return "yes found"
    return "not found", 404


@app.route("/now")
def now():
    return "Gone", 410


@app.route("/contact")
@app.route("/herd.html")
def redir_index():
    """
    Redirects for things that have now been merged into the index
    """
    return redirect(url_for("index"), code=301)
