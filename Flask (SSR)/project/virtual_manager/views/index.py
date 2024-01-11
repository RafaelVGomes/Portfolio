from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from virtual_manager.db import get_db
from virtual_manager.views.auth import login_required


bp = Blueprint('index', __name__)

@bp.route("/")
@login_required
def index():
  """Show portfolio of stocks"""
  db = get_db()
  USER_ID = session['user_id']
  # cash = db.execute("SELECT cash FROM business;")[0]['cash']
  items = db.execute("SELECT * FROM items;")
  products = db.execute("SELECT * FROM products;")
  recipes = db.execute("SELECT * FROM recipes;")

  data = {
      'cash': 0,
      'products': products,
      'purchases_total': 0,
      'overall': 0
  }
  # TODO: Fix this declaration
  # data['overall'] = data['purchases_total'] + data['cash']

  # if request.args['data'] == 'table':
  #   return render_template("index/index_table.html", data=data)
  # else:
  return render_template("index/index.html", data=data, items=items, products=products)
  