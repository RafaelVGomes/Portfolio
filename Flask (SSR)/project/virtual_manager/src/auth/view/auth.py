import functools
import json
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


bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../html', static_folder='../../auth')

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
    form = request.form
    data = {
      'username': form.get('username').lower(),
      'password': form.get('password'),
      'confirmation': form.get('confirmation'),
      'errors': 0
    }
    
    if not data['username']:
      flash('Username is required.', 'username')
      data['errors'] += 1

    u = get_db().execute("SELECT username FROM users WHERE username = ?", (data['username'],)).fetchone()
    if u:
      u = u['username']
    
    if u == data['username']:
      flash('Username unavailable.', 'username')
      data['errors'] += 1
    
    if not data['password']:
      flash('Password is required.', 'password')
      data['errors'] += 1
    
    if not data['confirmation']:
      flash('Password confirmation is required.', 'confirmation')
      data['errors'] += 1
    elif data['password'] != data['confirmation']:
      flash("Password confirmation doesn't match.", 'confirmation')
      data['errors'] += 1

    if data['errors']:
      return render_template('register.html', data=data)
    else:
      db = get_db()
      data['password'] = generate_password_hash(data['password'])
      try:
        db.execute(
          "INSERT INTO users (username, hash) VALUES (:username, :password)",
          (data),
        )
        db.commit()
      except db.IntegrityError:
        flash(f"User {data['username']} is already registered.", 'username')
      else:
        return redirect(url_for("auth.login"))
  
  q = request.args.get('q')
  if q:
    if len(q) < 3:
      return json.dumps("4 or more letters.")
    
    u = get_db().execute("SELECT username FROM users WHERE username = ?", (q.lower(),)).fetchone()
    if u:
      u = u['username']
    
    return ('false', 'true')[q == u]
  else:
    return render_template('register.html')


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
    # TODO: implement new error handler
    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))

    flash(error)

  return render_template('login.html')


@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))