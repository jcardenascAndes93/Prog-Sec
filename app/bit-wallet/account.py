import os
from flask import Blueprint, flash, current_app, g, redirect, render_template, request, url_for, send_from_directory
from werkzeug.exceptions import abort
from .db import get_db

bp = Blueprint('account', __name__)


@bp.route('/profile/<username>')
def profile(username):
    """ Show the user's profile, picture and posts. """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = 'SELECT * FROM user WHERE username = "' + username + '"'
    cursor.execute(query)
    user = cursor.fetchone()
    picture = None
    posts = None

    if user is not None:
        picture = user["picture_filename"]
        cursor = get_db().cursor(dictionary=True)
        query = 'SELECT * FROM post WHERE author_id = "' + str(user['id']) + '"' \
                ' ORDER BY created DESC'
        cursor.execute(query)
        posts = cursor.fetchall()
    return render_template('account/profile.html', username=username, picture=picture, posts=posts)


@bp.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(
        os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER']),
        filename,
    )


@bp.route('/upload/<username>', methods=['POST'])
def upload_picture(username):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # Save file locally
        file.save(os.path.join(
            os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER']),
            file.filename,
        ))

        # Update user with picture url
        db = get_db()
        query = 'UPDATE user SET picture_filename = "' + file.filename + '" WHERE username = "' + username + '"'
        db.cursor().execute(query)
        db.commit()

        return redirect(url_for('account.profile', username=username))
