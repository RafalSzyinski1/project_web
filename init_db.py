import time
from security import create_app, db, bcrypt
from security.models.models import User, Key, Lock, KeyUsageHistory

app = create_app()


def init_users():
    db.session.add(User(name="Tom", surname="BB", email="Tom@demo.com",
                   password=bcrypt.generate_password_hash("pass"), is_admin=True))
    db.session.add(User(name="Ben", surname="AA", email="Ben@demo.com",
                   password=bcrypt.generate_password_hash("pass"), is_admin=True))
    db.session.add(User(name="Jeff", surname="CC", email="Jeff@demo.com",
                   password=bcrypt.generate_password_hash("pass"), is_admin=False))
    db.session.commit()


def init_key():
    for i in range(30):
        db.session.add(Key(name=f"Key{i+1}"))
    db.session.commit()


def init_locks():
    for i in range(30):
        db.session.add(Lock(name=f"Door{i+1}"))
    db.session.commit()


def init_history():
    for _ in range(1, 20):
        for i in range(1, 30):
            db.session.add(KeyUsageHistory(key_id=i, lock_id=i))
        db.session.commit()


def init_db_default():
    init_users()
    init_key()
    init_locks()
    init_history()


with app.app_context():
    db.drop_all()
    db.create_all()
    init_db_default()
