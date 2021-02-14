import pytest
import mysql.connector
import werkzeug.routing
from sc_blog.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        cursor = get_db().cursor()
        cursor.execute('SELECT COUNT(id) FROM post')
        [(count,)] = cursor.fetchall()
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        cursor = get_db().cursor(dictionary=True)
        cursor.execute('SELECT * FROM post WHERE id = 1')
        post = cursor.fetchone()
        assert post['title'] == 'updated'


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers.get('Location') == 'http://localhost/'

    with app.app_context():
        cursor = get_db().cursor(dictionary=True)
        cursor.execute('SELECT * FROM post WHERE id = 1')
        post = cursor.fetchone()
        assert post is None
