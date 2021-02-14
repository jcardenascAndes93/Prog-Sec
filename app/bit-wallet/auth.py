import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Register a user in the database. Redirect to login page if there are no errors, else go back to register page.

    If the method is POST, extract the username and password fields,
    check if there is a user in the database with such username,
    if not, add the record to the database.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # check if the fields are filled
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            # establish a connection with the db
            cursor = db.cursor()
            query = 'SELECT id FROM user WHERE username = "' + username + '"'
            cursor.execute(query)
            # if there is a user previously registered with the same name report an error
            if cursor.fetchone() is not None:
                error = 'Error {}.'.format(username)

        if error is None:
            cursor = db.cursor()
            query = 'INSERT INTO user (username, password) VALUES ("' + username + '", "' + password + '")'
            cursor.execute(query)
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """ Grant access to a user, given that the credentials provided match a record stored in the database. """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        cursor = get_db().cursor(dictionary=True)
        query = 'SELECT * FROM user WHERE username = "' + username + '"'
        cursor.execute(query)
        user = cursor.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not user['password'] == password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """ Extract a user's data from the database, given that there is an id stored in the session object, and store it
    in the g object. """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = {}
    else:
        cursor = get_db().cursor(dictionary=True)
        query = 'SELECT * FROM user WHERE id = "' + str(user_id) + '"'
        cursor.execute(query)
        g.user = cursor.fetchone()


@bp.route('/logout')
def logout():
    """ Empty the session object, redirect to main page. """

    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """ Check if a user is loaded in the g object, return to login otherwise. """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user.get('id') is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
