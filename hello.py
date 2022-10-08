"""Imports"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    """Hello, World!

    Returns:
        str: Print Hello, World!
    """
    return 'Hello, World!'
