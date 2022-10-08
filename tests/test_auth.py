"""Imports"""
import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    """Test register

    Args:
        client (object): Client
        app (object): Application
    """
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    """Test register validate input

    Args:
        client (object): Client
        username (str): Username
        password (str): Password
        message (str): Message
    """
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    """Test login

    Args:
        client (object): Client
        auth (object): Authentication
    """
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    """Test login validate input

    Args:
        auth (object): Authentication
        username (str): Username
        password (str): Password
        message (str): Messaage
    """
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """Test logout

    Args:
        client (object): Client
        auth (object): Authentication
    """
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
