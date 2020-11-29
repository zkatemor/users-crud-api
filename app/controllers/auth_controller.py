import hashlib
from secrets import token_hex

from flask_restful import Resource, reqparse

from app.auth.handlers import auth
from models.token import Token
from db.setup import db


class AuthController(Resource):
    def create_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        return args['username'], args['password']

    @auth.login_required
    def get(self):
        try:
            return {
                "result": {
                    "message": "Hello, {}!".format(auth.current_user())
                }
            }
        except Exception as e:
            return {
                       "error": {
                           "message": str(e)
                       }
                   }, 422

    @auth.login_required
    def post(self):
        try:
            username, password = self.create_params()
            password_sha = hashlib.sha256(password.encode()).hexdigest()
            token = token_hex(16)

            auth = Token(user=username, password=password_sha, token=token)
            db.session.add(auth)
            db.session.commit()
            return {
                       "result": {
                           "token": token
                       }
                   }, 201
        except Exception as e:
            return {
                       "error": {
                           "message": str(e)
                       }
                   }, 422
