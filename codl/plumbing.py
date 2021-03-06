"""
legacy redirects and hacky routing
"""

from .codl import app
from flask import redirect, url_for, abort, request, send_from_directory, Response
import os


@app.route("/herd.html")
def redir_herd():
    return redirect(url_for("index"), code=301)


@app.route("/.well-known/keybase.txt", defaults={"filename": "keybase.txt"})
@app.route("/robots.txt", defaults={"filename": "robots.txt"})
@app.route("/humans.txt", defaults={"filename": "humans.txt"})
@app.route("/ssh", defaults={"filename": "authorized_keys", "mimetype": "text/plain"})
def send_from_static(filename, **kwargs):
    return send_from_directory(app.static_folder, filename, **kwargs)


@app.route("/pgp")
def pgp_key():
    return send_from_static(
        "codl.asc", mimetype="application/pgp-keys", as_attachment=True
    )


@app.route("/_/<int:timestamp>/<path:filename>")
def static_cachebust(timestamp, filename):
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


@app.context_processor
def replace_url_for():
    return dict(url_for=cachebust_url_for)


def cachebust_url_for(endpoint, **kwargs):
    if endpoint == "static":
        endpoint = "static_cachebust"
        path = os.path.join(app.static_folder, kwargs.get("filename"))
        kwargs["timestamp"] = int(os.stat(path).st_mtime)
    return url_for(endpoint, **kwargs)


@app.route("/.well-known/webfinger")
def webfinger():
    resource = request.args["resource"]
    if resource == "acct:codl@codl.fr":
        return redirect(
            "https://chitter.xyz/.well-known/webfinger?resource=acct%3Acodl%40chitter.xyz"
        )
        return "yes found"
    return "not found", 404


@app.route("/", methods=("DUMBASS",))
def dumbass():
    return Response("yahaha you found me", content_type="text/dumbass")


@app.route("/now")
def now():
    return "Gone", 410


@app.route("/contact")
def contact():
    return redirect(url_for("index"))
