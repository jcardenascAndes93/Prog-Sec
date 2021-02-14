import os
from flask import Flask
from . import db, auth, blog, account


def create_app(instance_path=None, test_config=None):
    """ Returns an app instance. """

    # create and configure the bit-wallet
    app = Flask(__name__, instance_path=instance_path)
    app.jinja_options["autoescape"] = None
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER='upload',
        MYSQL_HOST=os.getenv('MYSQL_HOST'),
        MYSQL_USER=os.getenv('MYSQL_USER'),
        MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD'),
        MYSQL_DATABASE=os.getenv('MYSQL_DATABASE'),
    )

    if test_config is not None:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder and the UPLOAD_FOLDER folder exist
    try:
        os.makedirs(os.path.join(app.instance_path, app.config['UPLOAD_FOLDER']))
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(account.bp)
    app.add_url_rule('/', endpoint='index')

    return app
