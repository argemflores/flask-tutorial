"""Imports"""
import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Test application

    Yields:
        object: Test application
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Test client

    Args:
        app (object): Test application

    Returns:
        client: Test client
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test runner

    Args:
        app (object): Test application

    Returns:
        object: Test runner
    """
    return app.test_cli_runner()


class AuthActions():
    """Authentication Actions
    """
    def __init__(self, client):
        """Initialize

        Args:
            client (object): Client
        """
        self._client = client

    def login(self, username='test', password='test'):
        """Log in

        Args:
            username (str, optional): Username. Defaults to 'test'.
            password (str, optional): Password. Defaults to 'test'.

        Returns:
            object: Login response
        """
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        """Log out

        Returns:
            object: Logout response
        """
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """Authentication

    Args:
        client (object): Client

    Returns:
        object: Authentication Actions
    """
    return AuthActions(client)
