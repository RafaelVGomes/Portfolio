import sqlite3

import click
from flask import current_app, g

def get_db():
  if 'db' not in g:
    g.db = sqlite3.connect(
      current_app.config['DATABASE'],
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row

  return g.db

def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()
      
def init_db():
  db = get_db()

  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
  """"Create tables if doesn't exists."""
  init_db()
  click.echo('Database initialized')

def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)

db = get_db()


# from cs50 import SQL
# # Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///stock.db")

# # Create users table
# db.execute("""--sql
#   CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     username TEXT NOT NULL,
#     hash TEXT NOT NULL
#   );
# """)

# # Create and populate business table
# db.execute("""--sql
#   CREATE TABLE IF NOT EXISTS business (
#     id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL DEFAULT "default",
#     cash NUMERIC NOT NULL DEFAULT 0
#   );
# """)

# business = db.execute("""--sql
#   SELECT COUNT(*) FROM business;
# """)

# if not business:
#   db.execute("""--sql
#     INSERT DEFAULT VALUES;
#   """)

# # Create items table and index
# db.execute("""--sql
#   CREATE TABLE IF NOT EXISTS items (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     item_name TEXT NOT NULL UNIQUE,
#     amount NUMERIC NOT NULL,
#     price NUMERIC NOT NULL,
#     sale_price NUMERIC,
#     is_product INTEGER NOT NULL,
#     quantity_alert INTEGER NOT NULL,
#     measure TEXT NOT NULL
#   );
# """)

# db.execute("""--sql
#   CREATE INDEX IF NOT EXISTS idx_items ON items (item_name);
# """)

# # Create products table and index
# db.execute("""--sql
#   CREATE TABLE IF NOT EXISTS products (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     product_name TEXT NOT NULL UNIQUE,
#     amount NUMERIC NOT NULL,
#     measure TEXT NOT NULL,
#     quantity_alert INTEGER,
#     price NUMERIC NOT NULL,
#     has_recipe INTEGER NOT NULL
#   );
# """)

# db.execute("""--sql
#   CREATE INDEX IF NOT EXISTS idx_product ON products (product_name);
# """)

# # Create recipes table and index
# db.execute("""--sql
#   CREATE TABLE IF NOT EXISTS recipes (
#     product_id INTEGER NOT NULL,
#     item_id INTEGER NOT NULL,
#     item_name TEXT NOT NULL,
#     amount NUMERIC NOT NULL,
#     FOREIGN KEY (product_id) REFERENCES products (id) ON UPDATE CASCADE ON DELETE CASCADE,
#     FOREIGN KEY (item_id) REFERENCES items (id) ON UPDATE CASCADE ON DELETE CASCADE
#   );
# """)

# db.execute("""--sql
#   CREATE INDEX IF NOT EXISTS idx_recipes ON recipes (product_id);
# """)

# # Create historic table and index
# db.execute("""--sql
#   CREATE TABLE IF NOT EXISTS historic (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     user_id INTEGER NOT NULL,
#     date TEXT DEFAULT CURRENT_TIMESTAMP,
#     trade TEXT NOT NULL,
#     price NUMERIC NOT NULL,
#     amount INTEGER NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
#   );
           
# """)
# db.execute("""--sql
#   CREATE INDEX IF NOT EXISTS idx_historic ON historic (user_id, trade);
# """)