import os
import pytest
from sc_blog import create_app
from sc_blog.db import get_db, init_db, close_db, clean_folder

UPLOAD_FOLDER = './test_upload'

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app(
        instance_path=os.getenv('TEST_INSTANCE_PATH'),
        test_config={
            'TESTING': True,
            'UPLOAD_FOLDER': 'test_upload',
            'MYSQL_HOST': os.getenv('MYSQL_HOST'),
            'MYSQL_USER': 'test',
            'MYSQL_PASSWORD': 'test',
            'MYSQL_DATABASE': 'test',
        }
    )

    with app.app_context():
        init_db()
        db = get_db()
        for result in db.cursor().execute(_data_sql, multi=True):
            print("Number of rows affected by statement '{}': {}".format(
                result.statement, result.rowcount))
        db.commit()

    yield app

    clean_folder(os.path.join(os.getenv('TEST_INSTANCE_PATH'), 'test_upload'))


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password},
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

