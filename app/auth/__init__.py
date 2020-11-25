from flask_httpauth import HTTPTokenAuth

from models.token import Token

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    query = Token.query.order_by(Token.id).all()

    tokens = dict()
    for tkn in query:
        tokens[tkn.token] = tkn.user

    if token in tokens:
        return tokens[token]
