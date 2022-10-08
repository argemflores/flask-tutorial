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

    test_app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield test_app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(test_app):
    """Test client

    Args:
        app (object): Test application

    Returns:
        client: Test client
    """
    return test_app.test_client()


@pytest.fixture
def runner(test_app):
    """Test runner

    Args:
        app (object): Test application

    Returns:
        object: Test runner
    """
    return test_app.test_cli_runner()
