"""Imports"""
import sqlite3

import click
from flask import current_app, g


def get_db():
    """Get database

    Returns:
        object: Database
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


def init_db():
    """Initialize database
    """
    db_conn = get_db()

    with current_app.open_resource('schema.sql') as file:
        db_conn.executescript(file.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Initialize application

    Args:
        app (object): Application
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
