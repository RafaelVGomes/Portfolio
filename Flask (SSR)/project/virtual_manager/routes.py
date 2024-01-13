# from flask import flash, redirect, render_template, request, session
# from werkzeug.security import check_password_hash, generate_password_hash

# from virtual_manager import create_app
# from virtual_manager.helpers import apology, login_required, usd, percent_diff
# from virtual_manager.db import db

# app = create_app()

# from virtual_manager.index import views

# @app.after_request
# def after_request(response):
#   """Ensure responses aren't cached"""
#   response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#   response.headers["Expires"] = 0
#   response.headers["Pragma"] = "no-cache"
#   return response

# # from virtual_manager.index.views import index
# # @app.route("/")(index)






# # Products routes
# @app.route("/products")
# @login_required
# def products():
#     """List all products on stock"""
#     products = db.execute("SELECT * FROM products;")
#     return render_template("products/products.html", products=products)


# @app.route("/add-product", methods=["GET", "POST"])
# @login_required
# def add_product():
#     """Add product to stock"""
#     if request.method == "GET":
#         items = db.execute("SELECT * FROM items;")
#         return render_template("products/product.html", items=items)
#     else:
#         USER_ID = session['user_id']
#         PROD_NAME = request.form.get("product_name").lower()
#         if PROD_NAME == "":
#             return apology("Please enter a product name")

#         AMOUNT = int(request.form.get("amount"))
#         if AMOUNT == "":
#             return apology("Please enter a amount")

#         MEASURE = request.form.get("measure")
#         if MEASURE == "":
#             return apology("Please choose a measure")
#         elif MEASURE not in ['Kg', 'L', 'Unit']:
#             return apology("Invalid measure")

#         QUANT_ALERT = request.form.get("quantity_alert")

#         PRICE = request.form.get("price")
#         if PRICE == "":
#             return apology("Please enter a price")

#         HAS_RECIPE = request.form.get("has_recipe")

#         INLINE_TOTAL = int(request.form.get("inlineFormsTotal"))

#         # CASH = round(float(AMOUNT) * float(PRICE), 2)
#         # db.execute("UPDATE business SET cash = business.cash - ?", CASH)

#         PROD_ID = db.execute("INSERT INTO products (product_name, amount, price, quantity_alert, measure, has_recipe) VALUES (?,?,?,?,?,?)", PROD_NAME, AMOUNT, PRICE, QUANT_ALERT, MEASURE, HAS_RECIPE)
#         #db.execute("INSERT INTO historic (user_id, trade, price, amount) VALUES (?,?,?,?)", USER_ID, "purchase", PRICE, AMOUNT)

#         for i in range(INLINE_TOTAL):
#             DATA = request.form.getlist(f"recipe_items_{i}")
#             ID_AND_NAME = DATA[0].split(',')
#             ITEM_ID = ID_AND_NAME[0]
#             ITEM_NAME = ID_AND_NAME[1]
#             ITEM_AMOUNT = DATA[1]

#             db.execute("INSERT INTO recipes (product_id, item_id, item_name, amount) VALUES (?,?,?,?)", PROD_ID, ITEM_ID, ITEM_NAME, ITEM_AMOUNT)
#             db.execute("UPDATE items SET amount = items.amount - ? WHERE id = ?", round(float(AMOUNT) * float(ITEM_AMOUNT), 1), ITEM_ID)

#         return redirect("/add-product")


# @app.route("/upd-product/<int:id>", methods=["GET", "POST"])
# @login_required
# def upd_product(id):
#     """Modify product from stock"""
#     if request.method == "GET":
#         product = db.execute("SELECT * FROM products WHERE id = ?;", id)[0]
#         items = db.execute("SELECT * FROM items;")
#         recipes = db.execute("SELECT * FROM recipes WHERE product_id = ?;", id)
#         return render_template("products/product.html", product=product, items=items, recipes=recipes)
#     else:
#         AMOUNT = request.form.get("amount")
#         if AMOUNT == "":
#             return apology("Please enter a amount")

#         MEASURE = request.form.get("measure")
#         if MEASURE == "":
#             return apology("Please choose a measure")
#         elif MEASURE not in ['Kg', 'L', 'Unit']:
#             return apology("Invalid measure")

#         QUANT_ALERT = request.form.get("quantity_alert")

#         PRICE = float(request.form.get("price"))
#         if PRICE == "":
#             return apology("Please enter a price")

#         HAS_RECIPE = request.form.get("has_recipe")

#         INLINE_TOTAL = int(request.form.get("inlineFormsTotal"))

#         INLINE_CREATED = request.form.get("createdInlineForms")

#         INLINE_DELETED = request.form.get("deletedInlineForms")

#         CREATE_LIST = []
#         if INLINE_CREATED:
#             for i in INLINE_CREATED.split(','):
#                 CREATE_LIST.append(f"recipe_items_{i}")

#         DELETE_LIST = []
#         if INLINE_DELETED:
#             for i in INLINE_DELETED.split(','):
#                 DELETE_LIST.append(f"recipe_items_{i}")

#         ITEMS = []
#         for i in range(INLINE_TOTAL):
#             DATA = request.form.getlist(f"recipe_items_{i}")

#             if not DATA or 'Select an item' in DATA:
#                 HAS_RECIPE = 0
#                 continue
#             else:
#                 ID_AND_NAME = DATA[0].split(',')
#                 ITEM_ID = ID_AND_NAME[0]
#                 ITEM_NAME = ID_AND_NAME[1]
#                 ITEM_AMOUNT = DATA[1]
#                 DATA = db.execute("SELECT amount, price FROM items WHERE id = ?", ITEM_ID)[0]
#                 ITEM_STOCK = DATA['amount']
#                 print('ITEM_AMOUNT:', ITEM_AMOUNT)
#                 print('ITEM_STOCK:', ITEM_STOCK)
#                 ITEM_PRICE = DATA['price']
#                 if float(ITEM_AMOUNT) > int(ITEM_STOCK):
#                     return apology(f'Not enough "{ITEM_NAME}"!')
#                 else:
#                     ITEMS.append({'id': ITEM_ID, 'name': ITEM_NAME, 'amount': float(ITEM_AMOUNT), 'price': float(ITEM_PRICE), 'stock': ITEM_STOCK, 'recipe': f"recipe_items_{i}"})

#         for ITEM in ITEMS:
#             if ITEM['recipe'] in CREATE_LIST:
#                 db.execute("INSERT INTO recipes (product_id, item_id, item_name, amount) VALUES (?,?,?,?)", id, ITEM['id'], ITEM['name'], ITEM['amount'])
#                 db.execute("UPDATE items SET amount = items.amount - ? WHERE id = ?", ITEM['amount'], ITEM['id'])
#                 #TODO: fix this increment to add only the difference
#                 db.execute("UPDATE business SET cash = business.cash - ?", ITEM['amount'] * ITEM['price'])
#             elif ITEM['recipe'] in DELETE_LIST:
#                 db.execute("DELETE FROM recipes WHERE item_id = ?", ITEM['id'])
#             else:
#                 #TODO: fix this increment to add only the difference
#                 db.execute("UPDATE recipes SET amount = ? WHERE item_id = ?", ITEM['amount'], ITEM['id'])
#                 db.execute("UPDATE items SET amount = items.amount - ? WHERE id = ?", round(float(AMOUNT) * ITEM['amount'], 2), ITEM['id'])

#         P = db.execute("SELECT product_name, amount FROM products WHERE id = ?", id)[0]
#         PROD_NAME = P['product_name']
#         PROD_STOCK = P['amount']
#         #TODO: fix this increment to add only the difference
#         # if float(AMOUNT) > float(PROD_STOCK):
#         #     db.execute("UPDATE business SET cash = business.cash - ?", round((float(PROD_STOCK) - float(AMOUNT)) * float(PRICE), 2))
#         # else:
#         #     return apology(f'Can not decrease "{PROD_NAME}" amount')

#         db.execute("UPDATE products SET amount = ?, measure = ?, quantity_alert = ?, price = ?, has_recipe = ? WHERE id = ?", AMOUNT, MEASURE, QUANT_ALERT, PRICE, HAS_RECIPE, id)

#         return redirect("/products")


# @app.route("/del-product/<int:id>")
# @login_required
# def del_product(id):
#     """Erase product from stock"""
#     db.execute("DELETE FROM products WHERE id = ?", id)
#     return redirect("/products")


# @app.route("/sale")
# @login_required
# def sale():
#     """View and sell products from stock"""
#     products = db.execute("SELECT * FROM products;")
#     if request.args.get('data') == 'table':
#         return render_template("stock/stock table.html", products=products)
#     else:
#         return render_template("stock/stock.html", products=products)


# @app.route("/sell/<int:id>", methods=['POST'])
# @login_required
# def sell(id):
#     """Sell products from stock"""
#     DATA = db.execute("SELECT amount, price FROM products WHERE id = ?", id)[0]
#     STOCK = DATA['amount']
#     PRICE = DATA['price']
#     AMOUNT = request.form.get(f"amount_sell_{id}")
#     if int(AMOUNT) > STOCK:
#         return apology("You're selling more than you have")

#     db.execute("UPDATE products SET amount = products.amount - ? WHERE id = ?", int(AMOUNT), id)
#     db.execute("UPDATE business SET cash = business.cash + ?", int(AMOUNT) * float(PRICE))
#     return redirect("/sale")


# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""
#     USER_ID = session['user_id']
#     historic = db.execute("SELECT datetime(date, 'localtime') AS date, trade, amount, price FROM historic WHERE user_id = ? ORDER BY date", USER_ID)

#     return render_template("history.html", historic=historic)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")


# @app.route("/logout")
# def logout():
#     """Log user out"""
#     # Forget any user_id
#     session.clear()
#     # Redirect user to login form
#     return redirect("/")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""
#     if request.method == "GET":
#         return render_template("register.html")
#     else:
#         username = request.form.get("username").lower()
#         usernameCheck = db.execute("SELECT username FROM users WHERE username = ?", username)
#         password = request.form.get("password")
#         confirmation = request.form.get("confirmation")
#         if not username:
#             return apology("Please enter a username")
#         if usernameCheck:
#             return apology("Username already in use")

#         if not password:
#             return apology("Please enter a password")

#         if not confirmation:
#             return apology("Please confirm your password")

#         if password != confirmation:
#             return apology("Password confirmation doesn't match")
#         else:
#             db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, generate_password_hash(password))

#         return redirect("/login")