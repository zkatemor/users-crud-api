from db.setup import db


class User(db.Model):
    """table with users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    is_active = db.Column(db.Boolean, nullable=False)

    def __init__(self,
                 username: str, first_name: str,
                 last_name: str, is_active: bool):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def __str__(self) -> str:
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active
        }
