import subprocess
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from .db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """ Collect all the posts from the database in the form of a list and render the index template with said list. """

    cursor = get_db().cursor(dictionary=True)
    query = 'SELECT p.id, title, body, created, author_id, username' \
            ' FROM post p JOIN user u ON p.author_id = u.id' \
            ' ORDER BY created DESC'
    cursor.execute(query)
    # store the query results in a list
    posts = cursor.fetchall()
    return render_template('auth/register.html')


def valid_title(title):
    """ Check if title is unique with binary script. """

    popen = subprocess.run(['bit-wallet/check_title_binary', title], stdout=subprocess.PIPE)
    output = popen.stdout
    output = output.decode('utf8').strip()
    if output != 'true':
        return False
    return True


@bp.route('/create', methods=('GET', 'POST'))
def create():
    """ Insert a post into the database after checking the title is valid. """

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        error = None

        if not title:
            error = 'Title is required.'
        elif not valid_title(title):
            error = 'Title already exists.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query = 'INSERT INTO post (title, body, author_id)' \
                    ' VALUES ("' + title + '", "' + body + '" , ' + str(g.user.get('id')) + ')'
            db.cursor().execute(query)
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(_id):
    """ Get a post from the database using its id as reference. """

    cursor = get_db().cursor(dictionary=True)
    query = 'SELECT p.id, title, body, created, author_id, username' \
            ' FROM post p JOIN user u ON p.author_id = u.id' \
            ' WHERE p.id = ' + str(_id)
    cursor.execute(query)
    post = cursor.fetchone()

    return post


@bp.route('/<_id>/update', methods=('GET', 'POST'))
def update(_id):
    """ Update post with a given id. """
    _id = int(_id)
    post = get_post(_id)

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query = 'UPDATE post SET title = "' + title + '", body = "' + body + '" WHERE id = ' + str(_id)
            db.cursor().execute(query)
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post if post is not None else {})


@bp.route('/<_id>/delete', methods=('POST',))
def delete(_id):
    """ Delete post with a given id. """
    _id = int(_id)
    # Complete code here
    return redirect(url_for('blog.index'))
