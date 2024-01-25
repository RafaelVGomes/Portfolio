-- database: ../instance/virtual_manager.sqlite
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  hash TEXT NOT NULL,
  is_active INTEGER DEFAULT 1,
  is_staff INTEGER DEFAULT 0,
  is_admin INTEGER DEFAULT 0,
  cash NUMERIC DEFAULT 0.00
);
CREATE INDEX idx_users ON users (id, username, is_active, is_staff);



CREATE TABLE items (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  item_name TEXT NOT NULL UNIQUE,
  amount NUMERIC NOT NULL DEFAULT 0,
  measure TEXT NOT NULL,
  quantity_alert INTEGER NOT NULL DEFAULT 0,
  price NUMERIC  DEFAULT 0,
  is_product INTEGER NOT NULL DEFAULT 0,
  sale_price NUMERIC DEFAULT "-",
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX idx_items ON items (id, item_name, is_product);

CREATE TABLE items_log (
  id INTEGER PRIMARY KEY,
  date TEXT DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER NOT NULL,
  operation TEXT NOT NULL,
  item_name TEXT NOT NULL,
  item_field TEXT DEFAULT "-",
  old_value TEXT DEFAULT "-",
  new_value TEXT DEFAULT "-",
  FOREIGN KEY (user_id) REFERENCES users (id)
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
);

CREATE INDEX idx_items_log ON items_log (id, date, user_id, item_name, operation);

CREATE TABLE items_history (
  id INTEGER PRIMARY KEY,
  date TEXT DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER NOT NULL,
  trade TEXT NOT NULL,
  amount TEXT NOT NULL,
  measure TEXT NOT NULL,
  item_name TEXT NOT NULL,
  price TEXT NOT NULL,
  total  NUMERIC NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
);

CREATE INDEX idx_items_history ON items_history (id, date, user_id, item_name, trade);


CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  product_name TEXT NOT NULL UNIQUE,
  amount NUMERIC NOT NULL,
  measure TEXT NOT NULL,
  quantity_alert INTEGER,
  price NUMERIC NOT NULL,
  has_recipe INTEGER NOT NULL
);

CREATE INDEX idx_product ON products (id, product_name);


CREATE TABLE recipes (
  product_id INTEGER PRIMARY KEY,
  item_id INTEGER NOT NULL,
  amount NUMERIC NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
  FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
);

CREATE INDEX idx_recipes ON recipes (product_id, item_id);
