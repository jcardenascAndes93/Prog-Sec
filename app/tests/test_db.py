import pytest
import mysql.connector
from sc_blog.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(mysql.connector.errors.OperationalError) as e:
        db.cursor().execute('SELECT 1')
    assert 'not available' in str(e.value)
