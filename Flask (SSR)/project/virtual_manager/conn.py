from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///stock.db")

db.execute("""--sql
  CREATE TABLE IF NOT EXISTS business (
    id INTEGER PRIMARY KEY,
    cash NUMERIC NOT NULL DEFAULT 0
  );
""")
if not db.execute("""--sql SELECT * FROM business;"""):
    db.execute("""--sql INSERT INTO business (cash) VALUES(0);""")

db.execute("""--sql
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
  );
""")

db.execute("""--sql
  CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    item_name TEXT NOT NULL UNIQUE,
    amount NUMERIC NOT NULL,
    price NUMERIC NOT NULL,
    sale_price NUMERIC,
    is_product INTEGER NOT NULL,
    quantity_alert INTEGER NOT NULL,
    measure TEXT NOT NULL
  );
""")
db.execute("""--sql CREATE INDEX IF NOT EXISTS idx_items ON items (item_name);""")

db.execute("""--sql
  CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    product_name TEXT NOT NULL UNIQUE,
    amount NUMERIC NOT NULL,
    measure TEXT NOT NULL,
    quantity_alert INTEGER,
    price NUMERIC NOT NULL,
    has_recipe INTEGER NOT NULL
  );
""")
db.execute("""--sql CREATE INDEX IF NOT EXISTS idx_product ON products (product_name);""")

db.execute("""--sql
  CREATE TABLE IF NOT EXISTS recipes (
    product_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items (id) ON UPDATE CASCADE ON DELETE CASCADE
  );
""")
db.execute("""--sql CREATE INDEX IF NOT EXISTS idx_recipes ON recipes (product_id);""")

db.execute("""--sql
  CREATE TABLE IF NOT EXISTS historic (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP,
    trade TEXT NOT NULL,
    price NUMERIC NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
  );
""")
db.execute("""--sql CREATE INDEX IF NOT EXISTS idx_historic ON historic (user_id, trade);""")