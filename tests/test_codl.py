from bs4 import BeautifulSoup
import re
from flask import url_for


def test_contact(client):
    resp = client.get(url_for('contact'))
    soup = BeautifulSoup(resp.get_data(as_text=True), 'html.parser')
    assert soup.find('a', href=re.compile(r'^mailto:'))
    assert soup.find('a', href=re.compile(r'^https://chitter\.xyz'))
