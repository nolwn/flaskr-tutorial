import sqlite3

import click # is for creating CLI interfaces

# current_app points to the flask application handling the request
# g—probably for "global"—holds variables that will be reused by many functions
from flask import current_app, g
from flask.cli import with_appcontext # I don't know what this is...

def get_db():
    if 'db' not in g: # has the database connection not already been made?
        g.db = sqlite3.connect( # then make it!
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES # some sqlite3 setting...
        )
        # Make sure rows are returns as dicts so they can be easily accessed.
        g.db.row_factory = sqlite3.Row

    return g.db

# Tells flask how to close a db connection so it can do so after each request
def close_db(e=None): # no idea what `e` is!
    db = g.pop('db', None) # None is a default return if `db` is not in g

    if db is not None:
        db.close() # close the connection

def init_db():
    db = get_db() # get the connection

    # `open_resource` opens a file relative to the flaskr package
    with current_app.open_resource('schema.sql') as file:
        db.executescript(file.read().decode('utf8'))

@click.command('init-db') # So we can run `flask init-db` from the CLI

# "Wraps a callback so that it’s guaranteed to be executed with the script’s
# application context. If callbacks are registered directly to the app.cli
# object then they are wrapped with this function by default unless it’s
# disabled." — Flask documentation
@with_appcontext
# For some reason, we are defining a differnt function to be decorated.
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

# the init function (duh!)
def init_app(app): # app, an instance of our application
    app.teardown_appcontext(close_db) # Gives the app db shutdown instructions
    app.cli.add_command(init_db_command) # adds our cli command to flask
