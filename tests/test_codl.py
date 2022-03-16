from bs4 import BeautifulSoup
import re
from flask import url_for


def test_index(client):
    resp = client.get(url_for("index"), follow_redirects=True)
    soup = BeautifulSoup(resp.get_data(as_text=True), "html.parser")
    assert soup.find("a", href=re.compile(r"^mailto:")) is not None
    assert (
        soup.find("a", href=re.compile(r"^https://chitter\.xyz"), rel="me") is not None
    )
