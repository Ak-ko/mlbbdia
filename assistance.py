import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# def coins(c):
#     """Look up quote for symbol."""

#     # Contact API
#     try:
#         url = https://ide.cs50.io/01be96522f6b41d7a41a0f7094a7f97f/templates/index.html
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.RequestException:
#         return None

#     # Parse response
#     try:
#         myCoin = response.json()
#         return {
#             "coins" : myCoin["coins"]
#         }
#     except (KeyError, TypeError, ValueError):
#         return None

