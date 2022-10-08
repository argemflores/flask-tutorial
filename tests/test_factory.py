"""Imports"""
from flaskr import create_app


def test_config():
    """Test configuration
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    """Test Hello World

    Args:
        client (bool): True if pass; False if otherwise
    """
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
