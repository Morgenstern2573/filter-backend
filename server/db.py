from flask import current_app, g
import sqlite3


def get_db():
    if not 'db' in g:
        g.db = sqlite3.connect(
            './db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
