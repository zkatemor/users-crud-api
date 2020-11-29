from flask_httpauth import HTTPTokenAuth

from models.token import Token

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    query = Token.query.filter(Token.token == token).first()
    if query is not None:
        return query.user
