from flask import Blueprint, flash, redirect, render_template, request, g, url_for

from virtual_manager.db import get_db
from virtual_manager.helpers import updated_columns
from virtual_manager.src.auth.view.auth import login_required


bp = Blueprint('products', __name__, url_prefix='/products', template_folder='../html', static_folder='../../products', static_url_path='/')

@bp.route("/overview")
@login_required
def overview():
  """List all products on stock"""
  db = get_db()
  user_id = g.user['id']
  products = db.execute("SELECT * FROM products WHERE user_id = ?;", (user_id,)).fetchall()
  return render_template("products.html", products=products)


@bp.route("/create-product", methods=["GET", "POST"])
@login_required
def create_product():
  """Create product"""
  if request.method == "POST":
    data = {
      'product_name': request.form.get("product_name"),
      'amount': request.form.get("amount", type=int),
      'measure': request.form.get("measure"),
      'quantity_alert': request.form.get("quantity_alert", type=int),
      'price': request.form.get("price", type=float),
      'has_recipe': request.form.get("has_recipe", type=int),
      'inline_total': request.form.get("inlineFormsTotal", type=int),
      'errors': 0
    }

    if not data['product_name']:
      flash("Please enter an product name.", 'product_name')
      data['errors'] += 1

    if not data['amount']:
      flash("Please enter an amount.", 'amount')
      data['errors'] += 1
      
    if not data['measure']:
      flash("Please select a measure.", 'measure')
      data['errors'] += 1
    elif data['measure'] not in ['Kg', 'L', 'Unit']:
      flash("Invalid measure.", 'measure')
      data['errors'] += 1

    if not data['quantity_alert']:
      flash("Please enter a quantity alert.", 'quantity_alert')
      data['errors'] += 1

    if not data['price']:
      flash("Please enter a price.", 'price')
      data['errors'] += 1

    if data['has_recipe'] not in [0, 1]:
      flash("Invalid option.", 'has_recipe')
      data['errors'] += 1

    if data['has_recipe'] == 1 and not data['sale_price']:
      flash("Please enter a sale price.", 'sale_price')
      data['errors'] += 1

    
    if data['errors']:
      return render_template("create-product.html", data=data)
    else:
      db = get_db()
      data['user_id'] = g.user['id']
      
      prod_id = db.execute(
        """--sql
        INSERT INTO products (user_id, product_name, amount, measure, quantity_alert, price, has_recipe)
        VALUES (:user_id, :product_name, :amount, :measure, :quantity_alert, :price, :has_recipe);
        """, (data)
      ).lastrowid
      
      # for i in range(data['inline_total']):
      #   inline_forms = request.form.getlist(f"recipe_items_{i}")
      #   id_and_name = inline_forms[0].split(',')
      #   item_id = id_and_name[0]
      #   item_name = id_and_name[1]
      #   item_amount = inline_forms[1]

      #   db.execute("INSERT INTO recipes (product_id, item_id, item_name, amount) VALUES (?,?,?,?)", prod_id, item_id, item_name, item_amount)
      #   db.execute("UPDATE items SET amount = items.amount - ? WHERE id = ?", round(data['amount'] * item_amount, 1), item_id)

      # db.execute(
      #   """--sql
      #   INSERT INTO products_log (user_id, operation, product_name)
      #   VALUES (:user_id, 'created', :product_name);
      #   """, (data)
      # )

      # data['total'] = data['amount'] * data['price']
      # db.execute(
      #   """--sql
      #   INSERT INTO products_history (user_id, product_name, trade, price, amount, measure, total)
      #   VALUES (:user_id, :product_name, 'purchase', :price, :amount, :measure, :total)
      #   """, (data)
      # )
      
      # purchase_value = round(data['amount'] * data['price'], 2)
      # db.execute("UPDATE users SET cash = users.cash - ? WHERE id = ?", (purchase_value, data['user_id']))

      db.commit()
      return redirect(url_for("products.create_product"))
    
  return render_template("create-product.html")


@bp.route("/update-item/<int:id>", methods=["GET", "POST"])
@login_required
def update_item(id):
  """Modify item"""
  db = get_db()
  item = db.execute("SELECT * FROM items WHERE id = ?;", (id,)).fetchone()

  if request.method == "POST":
    data = {
      'amount': request.form.get("amount", type=int),
      'measure': request.form.get("measure"),
      'quantity_alert': request.form.get("quantity_alert", type=int),
      'price': request.form.get("price", type=float),
      'sale_price': request.form.get("sale_price", type=float),
      'has_recipe': request.form.get("has_recipe", type=int),
      'errors': 0
    }
    
    if not data['amount']:
      flash("Please enter a amount", 'amount')
      data['errors'] += 1
    
    if not data['measure']:
      flash("Please choose a measure", 'measure')
      data['errors'] += 1
    
    if not data['quantity_alert']:
      flash("Please enter an alert quantity", 'quantity_alert')
      data['errors'] += 1
    
    if not data['price']:
      flash("Please enter a price", 'price')
      data['errors'] += 1
    
    if data['is_product'] == 1 and not data['sale_price']:
      flash("Please enter a sale price", 'sale_price')
      data['errors'] += 1

    if data['errors']:
      return render_template("update-item.html", item=data)
    else:
      data['id'] = id
      db.execute(
        """--sql
        UPDATE items SET amount = :amount, price = :price, quantity_alert = :quantity_alert, measure = :measure, is_product = :is_product, sale_price = :sale_price WHERE id = :id;
        """, (data)
      )

      data['user_id'] = g.user['id']
      data['item_name'] = item['item_name']
      for col, values in updated_columns(item, data).items():
        data['item_field'] = col
        data['old_value'] = values['old']
        data['new_value'] = values['new']

        db.execute(
          """--sql
          INSERT INTO items_log (user_id, operation, item_name, item_field, old_value, new_value)
          VALUES (:user_id, 'updated', :item_name, :item_field, :old_value, :new_value);
          """, (data)
        )

      db.commit()
      return redirect(url_for("items.overview"))
  
  return render_template("update-item.html", item=item)


@bp.route("/delete-item/<int:id>")
@login_required
def delete_item(id):
    """Erase item"""
    # TODO: control who can delete items
    data = {}
    db = get_db()

    data['user_id'] = g.user['id']
    data['item_name'] = db.execute("SELECT item_name FROM items WHERE id = ?", (id,)).fetchone()['item_name']
    
    db.execute("DELETE FROM items WHERE id = ?", (id,))
    
    db.execute(
        """--sql
        INSERT INTO items_log (user_id, operation, item_name)
        VALUES (:user_id, 'deleted', :item_name);
        """, (data)
      )
    
    db.commit()
    return redirect(url_for("items.overview"))

@bp.route("/history")
@login_required
def history():
  """Historic of purchases and sales"""
  db = get_db()
  history = db.execute(
    """--sql
      SELECT DATETIME(h.date, 'localtime') as date, u.username, h.item_name, h.trade, h.price, h.amount, h.measure, h.total FROM users as u, items_history as h WHERE h.user_id = u.id AND u.id = ?;
    """,
    (g.user['id'],)
  ).fetchall()
  return render_template("items-history.html", history=history)

@bp.route("/log")
@login_required
def log():
  """Historic of purchases and sales"""
  db = get_db()
  log = db.execute(
    """--sql
      SELECT DATETIME(l.date, 'localtime') as date, u.username, l.item_name, l.operation, l.item_field, l.old_value, l.new_value FROM users as u, items_log as l WHERE l.user_id = u.id AND u.id = ?;
    """,
    (g.user['id'],)
  ).fetchall()
  return render_template("items-log.html", log=log)