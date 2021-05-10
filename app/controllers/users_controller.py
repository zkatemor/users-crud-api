from http import HTTPStatus

from flask_restful import Resource, reqparse

from app.auth.handlers import auth
from app.entities.basic_error import BasicError
from app.entities.basic_schema import BasicSchema, BasicResponseSchema
from models.user import User
from db.setup import db


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
        username, first_name, last_name, is_active = self.create_params()
        user = User(username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=is_active)
        db.session.add(user)
        db.session.commit()

        user_json = User.serialize(user)
        response = BasicSchema(result=user_json, status_code=HTTPStatus.CREATED)
        return response.make_response(BasicResponseSchema().dump(response))

    @auth.login_required
    def get(self):
        query = User.query.order_by(User.id).all()
        user_json = [User.serialize(user) for user in query]
        response = BasicSchema(result=user_json)
        return BasicResponseSchema().dump(response)


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
            user_json = User.serialize(user)
            response = BasicSchema(result=user_json, status_code=HTTPStatus.CREATED)
            return response.make_response(BasicResponseSchema().dump(response))
        else:
            raise BasicError(message='Users not found', status=HTTPStatus.NOT_FOUND)

    @auth.login_required
    def get(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            user_json = User.serialize(user)
            response = BasicSchema(result=user_json)
            return BasicResponseSchema().dump(response)
        except Exception as e:
            raise BasicError(message='User not found', status=HTTPStatus.NOT_FOUND)

    @auth.login_required
    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            User.query.filter(User.id == id).delete()
            db.session.commit()
            return '', HTTPStatus.NO_CONTENT
        else:
            raise BasicError(message='User not found', status=HTTPStatus.NOT_FOUND)
