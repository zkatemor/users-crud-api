from flask_restful import Resource, reqparse

from models.user import User, db


class UsersController(Resource):
    def create_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('first_name', type=str, required=False)
        parser.add_argument('last_name', type=str, required=False)
        parser.add_argument('is_active', type=bool, required=True)
        args = parser.parse_args()
        return args['username'], args['first_name'], args['last_name'], args['is_active']

    def body_schema(self, user):
        return {"result": {'id': user.id,
                           'username': user.username,
                           'first_name': user.first_name,
                           'last_name': user.last_name,
                           'is_active': user.is_active,
                           'is_superuser': user.is_superuser}}

    def schema(self, users):
        return {"result": [{'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'is_active': user.is_active,
                            'is_superuser': user.is_superuser} for user in users]}

    def post(self):
        try:
            username, first_name, last_name, is_active = self.create_params()
            user = User(username=username, first_name=first_name, last_name=last_name, is_active=is_active)
            db.session.add(user)
            db.session.commit()
            return self.body_schema(user), 201
        except Exception as e:
            return {
                       "error": {
                           "message": str(e)
                       }
                   }, 422

    def get(self):
        query = User.query.order_by(User.id).all()
        data = self.schema(query)
        return data, 200
