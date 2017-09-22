import misaka
from flask import render_template_string, Markup


def render_markdown(template, **kwargs):
    with open('templates/{}'.format(template)) as f:
        html = misaka.html(f.read())
    return render_template_string('''
        {% extends "layout/default.html" %}
        {% block body %}
        {{ content }}
        {% endblock %}
            ''', content=Markup(html), **kwargs)
