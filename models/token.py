from db.setup import db


class Token(db.Model):
    """table with tokens"""
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    token = db.Column(db.String(150))

    def __init__(self, user: str, password: str, token: str):
        self.user = user
        self.password = password
        self.token = token
