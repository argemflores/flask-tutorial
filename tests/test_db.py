"""Imports"""
import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    """Test close database connection

    Args:
        app (bool): True if pass; False if otherwise
    """
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """Test initialize database

    Args:
        runner (object): Test runner
        monkeypatch (object): Monkeypatch
    """
    class Recorder(object):
        """Recorder

        Args:
            object (object): Object
        """
        called = False

    def fake_init_db():
        """Fake initial database
        """
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
