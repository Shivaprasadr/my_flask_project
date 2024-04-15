import mysql.connector
from flask import current_app, g
from mysql.connector import Error
import click

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                port=current_app.config['MYSQL_PORT'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB']
            )
            g.db.autocommit = True
        except Error as e:
            print("Error connecting to MySQL:", e)
            raise e
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        sql_statements = f.read().decode('utf-8').split(';')
        for statement in sql_statements:
            if statement.strip():
                cursor.execute(statement)
    db.commit()
    #cursor.close()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)