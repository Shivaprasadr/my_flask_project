from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
import logging
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from mysql.connector.errors import IntegrityError
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute(
                    "INSERT INTO user (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except IntegrityError:
                error = f"User {username} is already registered."
            finally:
                cursor.close()

            if error is None:
                return redirect(url_for("auth.login"))

        if error:
            flash(error)

    return render_template('auth/register.html', error=error)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            logging.info(f"Attempting to fetch user with username: {username}")
            
            try:
                cursor.execute('SELECT * FROM `user` WHERE username = %s', (username,))
                user = cursor.fetchone()
                logging.info(f"User fetched from database: {user}")
            except Exception as e:
                logging.error(f"Error executing query: {e}")
                user = None

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                current_app.logger.info(f"Session user_id set to {user['id']}")
                print(f"Session after setting user_id: {session}")
                return redirect(url_for('index'))
        finally:
            cursor.close()

        if error:
            flash(error)

    return render_template('auth/login.html', error=error)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM user WHERE id = %s', (user_id,)
        )
        g.user = cursor.fetchone()
        cursor.close()

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
