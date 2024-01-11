CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    is_staff INTEGER DEFAULT 0,
    is_admin INTEGER DEFAULT 0,
    cash NUMERIC DEFAULT 0.00
);
CREATE INDEX idx_users ON users (id, username, is_active);


CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL UNIQUE,
    amount NUMERIC NOT NULL,
    price NUMERIC NOT NULL,
    sale_price NUMERIC,
    is_product INTEGER NOT NULL,
    quantity_alert INTEGER NOT NULL,
    measure TEXT NOT NULL
);
CREATE INDEX idx_items ON items (id, item_name, is_product);


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


CREATE TABLE historic (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP,
    trade TEXT NOT NULL,
    price NUMERIC NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX idx_historic ON historic (user_id, date, trade);