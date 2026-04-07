import api.db as db


def test_db_init_and_insert(tmp_path, monkeypatch):
    """ Simple test for pytest on the database module."""
    db_path = tmp_path / "predictions.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)

    db.init_db()
    assert db_path.exists()

    db.log_single(100.0, 3, 2, 123456.0)
    db.log_batch(10, 234567.0)
