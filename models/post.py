from db.setup import db


class Post(db.Model):
    """table with posts"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __init__(self, userId, title, body):
        self.userId = userId
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Post %r>' % self.body

    def __str__(self):
        return self.body

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'user_id': self.userId
        }
