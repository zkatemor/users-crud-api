from http import HTTPStatus

from flask_restful import Resource, reqparse

from app.auth.handlers import auth
from app.entities.basic_error import BasicError
from app.entities.basic_schema import BasicSchema, BasicResponseSchema
from models.post import Post
from db.setup import db
from models.user import User


class PostssController(Resource):
    def create_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('body', type=str, required=True)
        parser.add_argument('userId', type=str, required=True)
        args = parser.parse_args()
        return args['title'], args['body'], args['userId']

    @auth.login_required
    def post(self):
        title, body, userId = self.create_params()
        post = Post(title=title, body=body, userId=userId)
        db.session.add(post)
        db.session.commit()

        post_json = Post.serialize(post)
        response = BasicSchema(result=post_json, status_code=HTTPStatus.CREATED)
        return response.make_response(BasicResponseSchema().dump(response))

    @auth.login_required
    def get(self):
        query = Post.query.order_by(Post.id).all()
        posts_json = [Post.serialize(q) for q in query]
        response = BasicSchema(result=posts_json)
        return BasicResponseSchema().dump(response)


class PostsIndexController(Resource):
    def update_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=False)
        parser.add_argument('body', type=str, required=False)
        parser.add_argument('userId', type=str, required=False)
        args = parser.parse_args()
        return args['title'], args['body'], args['userId']

    @auth.login_required
    def put(self, id):
        title, body, userId = self.update_params()

        post = Post.query.filter(Post.id == id).first()
        if post is not None:
            if title:
                Post.query.filter_by(id=id).update({'title': title})

            if body:
                Post.query.filter_by(id=id).update({'body': body})

            if userId:
                Post.query.filter_by(id=id).update({'userId': userId})

            db.session.commit()
            post = Post.query.filter(Post.id == id).first()

            db.session.commit()
            post_json = Post.serialize(post)
            response = BasicSchema(result=post_json)
            return BasicResponseSchema().dump(response)
        else:
            raise BasicError(message='Post not found', status=HTTPStatus.NOT_FOUND)

    @auth.login_required
    def get(self, id):
        try:
            post = Post.query.filter_by(id=id).first()
            post_json = Post.serialize(post)
            response = BasicSchema(result=post_json)
            return BasicResponseSchema().dump(response)
        except Exception as e:
            raise BasicError(message='Post not found', status=HTTPStatus.NOT_FOUND)

    @auth.login_required
    def delete(self, id):
        post = Post.query.filter(Post.id == id).first()
        if post is not None:
            Post.query.filter(Post.id == id).delete()
            db.session.commit()
            return '', HTTPStatus.NO_CONTENT
        else:
            raise BasicError(message='Post not found', status=HTTPStatus.NOT_FOUND)


class UserPost(Resource):
    @auth.login_required
    def get(self, userId):
        """viewing posts of a specific user"""
        if Post.query.filter(Post.userId == userId).count():
            posts = Post.query.filter(Post.userId == userId)
            posts_json = [Post.serialize(q) for q in posts]
            response = BasicSchema(result=posts_json)
            return BasicResponseSchema().dump(response)
        else:
            raise BasicError(message='Posts not found', status=HTTPStatus.NOT_FOUND)

    @auth.login_required
    def delete(self, userId):
        """delete specific user posts"""
        if Post.query.filter(Post.userId == userId).count():
            Post.query.filter(Post.userId == userId).delete()
            db.session.commit()
            return '', HTTPStatus.NO_CONTENT
        else:
            raise BasicError(message='Users not found', status=HTTPStatus.NOT_FOUND)


class Author(Resource):
    @auth.login_required
    def get(self, id):
        """found author of the post by post id"""
        user = User.query.join(User.posts, aliased=True) \
            .filter_by(id=id)

        user_json = User.serialize(user)
        response = BasicSchema(result=user_json)
        return BasicResponseSchema().dump(response)
