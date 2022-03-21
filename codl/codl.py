"""
Main pages go here
"""
from flask import Flask, render_template, make_response
import importlib
from mastodon import Mastodon
import redis
import pickle
from typing import Optional
import requests
import os

app = Flask(__name__)

DEFAULT_CONFIG = dict(
    DONPHAN_ACCESS_TOKEN=None,
    REDIS_HOST="127.0.0.1",
    REDIS_PORT=6379,
    REDIS_DB=0,
)
for key in DEFAULT_CONFIG:
    app.config[key] = os.getenv(key, DEFAULT_CONFIG[key])

importlib.import_module("codl.plumbing")


class NoMastodonAccess(Exception):
    pass


redis_conn: Optional[redis.Redis] = None


def get_redis() -> redis.Redis:
    """Instanciate redis client or return existing"""
    global redis_conn
    if not redis_conn:
        host = app.config.get("REDIS_HOST", "127.0.0.1")
        port = app.config.get("REDIS_PORT", "6379")
        db = app.config.get("REDIS_DB", "0")
        redis_conn = redis.Redis(host=host, port=port, db=db)

    return redis_conn


def recent_artworks(count=7) -> list[tuple[str, str]]:
    """
    Return a list of (post_url, thumbnail_url) tuples for recent public media
    posts on donphan, with the most popular (most faves) closer to the middle
    """
    CACHE_KEY = "www.codl.fr:4:artworks:{}".format(count)
    r = get_redis()
    cached = r.get(CACHE_KEY)
    if not cached:
        access_token = app.config.get("DONPHAN_ACCESS_TOKEN")
        if not access_token:
            raise NoMastodonAccess()

        session = requests.Session()
        session.headers.update({"user-agent": "www.codl.fr"})
        m = Mastodon(
            access_token=access_token,
            api_base_url="https://donphan.social/",
            session=session,
        )

        me = m.me()
        statuses = m.account_statuses(
            me["id"], only_media=True, exclude_replies=True, limit=40
        )
        artworks = list()
        for status in filter(
            lambda a: not a["sensitive"] and a["visibility"] == "public",
            sorted(statuses, key=lambda a: a["favourites_count"], reverse=True),
        ):
            artwork = (status["url"], status["media_attachments"][0]["preview_url"])
            artworks.append(artwork)
            artworks = list(reversed(artworks))
            if len(artworks) > count:
                break

        r.set(CACHE_KEY, pickle.dumps(artworks), ex=3600)

    else:
        artworks = pickle.loads(cached)

    return artworks


@app.route("/index.html")
@app.route("/")
def index():
    "Serves the index page."
    resp = make_response(render_template("index.html", artworks=recent_artworks()))
    resp.add_etag()
    return resp
