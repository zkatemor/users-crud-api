from http import HTTPStatus

from flask_restful import Resource, reqparse

from app.auth.handlers import auth
from models.user import User
from db.setup import db


def body_schema(user):
    return {"result": {'id': user.id,
                       'username': user.username,
                       'first_name': user.first_name,
                       'last_name': user.last_name,
                       'is_active': user.is_active}}


def schema(users):
    return {"result": [{'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_active': user.is_active} for user in users]}


class UsersController(Resource):
    def create_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('is_active', type=bool, required=True)
        args = parser.parse_args()
        return \
            args['username'], args['first_name'], \
            args['last_name'], args['is_active']

    @auth.login_required
    def post(self):
        try:
            username, first_name, last_name, is_active = self.create_params()
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        is_active=is_active)
            db.session.add(user)
            db.session.commit()
            return body_schema(user), HTTPStatus.OK
        except Exception as e:
            return {"error": {
                "message": str(e)
            }
                   }, HTTPStatus.UNPROCESSABLE_ENTITY

    @auth.login_required
    def get(self):
        query = User.query.order_by(User.id).all()
        data = schema(query)
        return data, HTTPStatus.OK


class UsersIndexController(Resource):
    def update_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=False)
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('is_active', type=bool, required=False)
        args = parser.parse_args()
        return \
            args['username'], args['first_name'], \
            args['last_name'], args['is_active']

    @auth.login_required
    def put(self, id):
        username, first_name, last_name, is_active = self.update_params()

        user = User.query.filter(User.id == id).first()
        if user is not None:
            if username:
                User.query.filter_by(id=id).update(
                    {'username': username})

            if first_name:
                User.query.filter_by(id=id).update(
                    {'first_name': first_name})

            if last_name:
                User.query.filter_by(id=id).update(
                    {'last_name': last_name})

            if is_active:
                User.query.filter_by(id=id).update(
                    {'is_active': is_active})

            db.session.commit()
            user = User.query.filter(User.id == id).first()

            db.session.commit()
            return body_schema(user), HTTPStatus.CREATED
        else:
            return {
                       "error": {
                           "message": 'User not found'
                       }
                   }, HTTPStatus.NOT_FOUND

    @auth.login_required
    def get(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            return body_schema(user), HTTPStatus.OK
        except Exception as e:
            return {
                       "error": {
                           "message": 'User not found'
                       }
                   }, HTTPStatus.NOT_FOUND

    @auth.login_required
    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            User.query.filter(User.id == id).delete()
            db.session.commit()
            return {"success": True}, HTTPStatus.OK
        else:
            return {
                       "error": {"message": "User not found"
                                 }
                   }, HTTPStatus.NOT_FOUND
