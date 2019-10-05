from flask import g
import sqlite3


def db():
    if 'db' not in g:
        g.db = sqlite3.connect('db_project.db')
        g.db.row_factory = sqlite3.Row

    return g.db
