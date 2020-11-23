from app import db


class User(db.Model):
    """table with users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    is_active = db.Column(db.Boolean, nullable=False)
    last_login = db.Column(db.DateTime)
    is_superuser = db.Column(db.Boolean)

    def __init__(self, username, first_name, last_name, is_active, last_login, is_superuser):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.last_login = last_login
        self.is_superuser = is_superuser

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return self.username
