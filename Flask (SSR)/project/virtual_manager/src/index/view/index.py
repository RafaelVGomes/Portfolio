from flask import Blueprint, flash, redirect, render_template, request, g, url_for

from virtual_manager.db import get_db
from virtual_manager.src.auth.view.auth import login_required


bp = Blueprint('index', __name__, template_folder='../html')

@bp.route("/")
@login_required
def index():
  """Show portfolio of stocks"""
  db = get_db()
  user_id = g.user['id']
  cash = db.execute("SELECT cash FROM users WHERE id = ?;", (user_id,)).fetchone()['cash']
  items = db.execute("SELECT * FROM items WHERE user_id = ?;", (user_id,)).fetchall()
  # products = db.execute("SELECT * FROM products;").fetchall()
  # recipes = db.execute("SELECT * FROM recipes;").fetchall()
  products = []
  return render_template("index.html", cash=cash, items=items, products=products)
  