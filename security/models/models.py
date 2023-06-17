from datetime import datetime

from security import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), nullable=False)
    surname = db.Column(db.String(254), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    image_file = db.Column(db.String(60), nullable=False,
                           default='default.jpg')

    keys = db.relationship('Key', backref='key_user', lazy=True)

    def admin_restart_password(self):
        new_pass = self.name[0] + self.surname
        self.password = bcrypt.generate_password_hash(new_pass)
        db.session.commit()

    def __repr__(self):
        return f"User({self.name} {self.surname})"


class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), nullable=False, unique=True)
    uid = db.Column(db.String(5), nullable=False, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    lock_to_key = db.relationship('KeyLocks', backref='key', lazy=True)
    key_usage = db.relationship('KeyUsageHistory', backref='key', lazy=True)

    def __repr__(self):
        return f"Key({self.name})"


class Lock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), nullable=False, unique=True)

    key_to_lock = db.relationship('KeyLocks', backref='lock', lazy=True)
    lock_usage = db.relationship('KeyUsageHistory', backref='lock', lazy=True)

    def __repr__(self):
        return f"Lock({self.name})"


class KeyLocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key_id = db.Column(db.Integer, db.ForeignKey('key.id'), nullable=False)
    lock_id = db.Column(db.Integer, db.ForeignKey('lock.id'), nullable=False)

    def __repr__(self):
        return f"KeyLock({self.key_id} - {self.lock_id})"


class KeyUsageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    key_id = db.Column(db.Integer, db.ForeignKey('key.id'), nullable=False)
    lock_id = db.Column(db.Integer, db.ForeignKey('lock.id'), nullable=False)

    def __repr__(self):
        return f"KeyUsageHistory({self.key_id} - {self.lock_id} | {self.date})"
