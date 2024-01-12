import functools
from flask import Blueprint, flash, redirect, render_template, request, session, g, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from virtual_manager.db import get_db

def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))
    return view(**kwargs)

  return wrapped_view


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form['username'].lower()
    password = request.form['password']
    confirmation = request.form['confirmation']
    db = get_db()
    error = None

    if not username:
      error = 'Username is required.'
    elif not password:
      error = 'Password is required.'
    elif not confirmation:
      error = 'Password confirmation is required.'
    elif password != confirmation:
      error = "Password confirmation doesn't match"

    if error is None:
      try:
        db.execute(
          "INSERT INTO users (username, hash) VALUES (?, ?)",
          (username, generate_password_hash(password)),
        )
        db.commit()
      except db.IntegrityError:
        error = f"User {username} is already registered."
      else:
        return redirect(url_for("auth.login"))

    flash(error)

  return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
      "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
      error = 'Incorrect username.'
    elif not check_password_hash(user['hash'], password):
      error = 'Incorrect password.'

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))

    flash(error)

  return render_template('auth/login.html')


@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))