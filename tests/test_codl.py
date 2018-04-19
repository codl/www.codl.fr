from bs4 import BeautifulSoup
import re
from flask import url_for


def strip_html(html):
    soup = BeautifulSoup(html, "html.parser")
    content = " ".join(soup.stripped_strings)
    content = re.sub('[\s]+', ' ', content)
    return content


def test_index(client):
    resp = client.get('/')
    assert "i'm codl" in strip_html(resp.get_data(as_text=True))


def test_contact(client):
    resp = client.get(url_for('contact'))
    soup = BeautifulSoup(resp.get_data(as_text=True), 'html.parser')
    assert soup.find('a', href=re.compile('^mailto:'))
    assert soup.find('a', href=re.compile('^https://chitter\.xyz'))
