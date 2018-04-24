"""
This code is used to store any helper functions...
"""
from flask import request, url_for


def redirect_url():
    return request.args.get('next') or \
            request.referrer or \
            url_for('index')
