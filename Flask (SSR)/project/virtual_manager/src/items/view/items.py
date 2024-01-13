from flask import Blueprint, flash, redirect, render_template, request, g, url_for

from virtual_manager.db import get_db
from virtual_manager.src.auth.view.auth import login_required


bp = Blueprint('items', __name__, url_prefix='/items')

@bp.route("/overview")
@login_required
def overview():
  """List all items on stock"""
  db = get_db()
  items = db.execute("SELECT * FROM items;").fetchall()
  return render_template("items/items.html", items=items)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
  """Add item to stock"""
  if request.method == "POST":
    user_id = g.user['id']
    prod_name = request.form.get("item_name")
    amount = request.form.get("amount", type=int)
    measure = request.form.get("measure")
    quant_alert = request.form.get("quantity_alert", type=int)
    price = request.form.get("price", type=float)
    sale_price = request.form.get("sale_price", type=float)
    is_prod = request.form.get("is_product", type=int)
    error = []
    
    if not prod_name:
      error = "Please enter a item name."
    elif not amount:
      error = "Please enter a amount."
    elif not measure:
      error = "Please choose a measure."
    elif measure not in ['Kg', 'L', 'Unit']:
      error = "Invalid measure."
    elif not quant_alert:
      error = "Please enter an alert quantity."
    elif not price:
      error = "Please enter a price."
    elif is_prod == 1 and not sale_price:
        error = "Please enter a sale price."

    if error:
      flash(error)
    else:
      db = get_db()
      cash = round(amount * price, 2)
      
      db.execute("INSERT INTO items (item_name, amount, price, is_product, quantity_alert, measure) VALUES (?,?,?,?,?,?)", (prod_name, amount, price, is_prod, quant_alert, measure))
      db.execute("INSERT INTO historic (user_id, trade, price, amount) VALUES (?,?,?,?)", (user_id, "purchase", price, amount))
      db.execute("UPDATE users SET cash = users.cash - ? WHERE id = 1", (cash,))
      db.commit()
      return redirect(url_for("items.add"))
    
  return render_template("items/item.html")


# @bp.route("/upd-item/<int:id>", methods=["GET", "POST"])
# @login_required
# def upd_item(id):
#     """Modify item from stock"""
#     db = get_db()

#     if request.method == "GET":
#         item = db.execute("SELECT * FROM items WHERE id = ?;", id)[0]
#         return render_template("items/item.html", item=item)
#     else:
#         AMOUNT = request.form.get("amount")
#         if AMOUNT == "":
#             return apology("Please enter a amount")

#         MEASURE = request.form.get("measure")
#         if MEASURE == "":
#             return apology("Please choose a measure")

#         QUANT_ALERT = request.form.get("quantity_alert")
#         if QUANT_ALERT == "":
#             return apology("Please enter an alert quantity")

#         PRICE = float(request.form.get("price"))
#         if PRICE == "":
#             return apology("Please enter a price")

#         # IS_PROD = request.form.get("is_product")

#         # SALE_PRICE = float(request.form.get("sale_price"))
#         # if IS_PROD == 1 and SALE_PRICE == "":
#         #     return apology("Please enter a sale price")

#         db.execute("UPDATE items SET amount = ?, price = ?, quantity_alert = ?, measure = ? WHERE id = ?", AMOUNT, PRICE, QUANT_ALERT, MEASURE, id)

#         return redirect("/items")


# @bp.route("/del-item/<int:id>")
# @login_required
# def del_item(id):
#     """Erase item from stock"""
#     db = get_db()

#     db.execute("DELETE FROM items WHERE id = ?", id)
#     return redirect("/items")