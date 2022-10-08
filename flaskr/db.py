"""Imports"""
import sqlite3

# import click
from flask import current_app, g


def get_db():
    """Get database

    Returns:
        db: Database
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(_error=None):
    """Close database connection

    Args:
        error (error, optional): Error. Defaults to None.
    """
    db_conn = g.pop('db', None)

    if db_conn is not None:
        db_conn.close()