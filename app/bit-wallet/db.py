import os
import shutil
import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext
from mysql.connector.constants import ClientFlag


def get_db():
    """ Establish a connection with the database and store it in the g object. """

    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DATABASE'],
            client_flags=[ClientFlag.MULTI_STATEMENTS]
        )

    return g.db


def close_db(e=None):
    """ Remove the database connection from the g object. """

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """ Execute the scheme currently stored in the resource sql file. """

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        cursor = db.cursor()
        schema = f.read().decode('utf8')
        for result in cursor.execute(schema, multi=True):
            if result.with_rows:
                print("Rows produced by statement '{}':".format(result.statement))
                print(result.fetchall())
            else:
                print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))


def clean_folder(path, e=None):
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    clean_folder(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER']))
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """ Close the db connection after returning a response, register the init_db_command to be used with the flask
    command. """

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
