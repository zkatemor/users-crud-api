from app import db


class User(db.Model):
    """table with users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    is_active = db.Column(db.Boolean, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)

    def __init__(self, username: str, first_name: str, last_name: str, is_active: bool,
                 is_superuser: bool = False):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_superuser = is_superuser

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def __str__(self) -> str:
        return self.username
