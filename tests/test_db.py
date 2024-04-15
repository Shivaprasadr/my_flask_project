import pytest
from flaskr.db import get_db, close_db, init_db


def test_get_close_db(app):

    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from user")
        result = cursor.fetchone()
        print("result for db qxecute is:", result)
        # Print the value of db to inspect its behavior
        print("Value of db is:", db)
        assert db is get_db()

    # Test that database is closed after the context ends
    with pytest.raises(Exception) as e:
        cursor = db.cursor()
        cursor.execute("select * from user")
    assert ' Connection not available.' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    print("result for initdb is:", result.output)
    print("result for recorder has been called:", Recorder.called)
    assert 'Initialized' in result.output
    assert Recorder.called