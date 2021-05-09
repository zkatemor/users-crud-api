from http import HTTPStatus

from flask_restful import Resource, reqparse

from app.auth.handlers import auth
from models.post import Post
from db.setup import db
from models.user import User


def body_schema(post):
    return {"result": {'id': post.id,
                       'title': post.title,
                       'body': post.body,
                       'userId': post.userId}}


def schema_users(users):
    return {"result": [{'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_active': user.is_active} for user in users]}


def schema(posts):
    return {"result": [{'id': post.id,
                        'title': post.title,
                        'body': post.body,
                        'userId': post.userId} for post in posts]}


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
        try:
            title, body, userId = self.create_params()
            post = Post(title=title, body=body, userId=userId)
            db.session.add(post)
            db.session.commit()
            return body_schema(post), HTTPStatus.CREATED
        except Exception as e:
            return {
                       "error": {
                           "message": str(e)
                       }
                   }, HTTPStatus.UNPROCESSABLE_ENTITY

    @auth.login_required
    def get(self):
        query = Post.query.order_by(Post.id).all()
        data = schema(query)
        return data, HTTPStatus.OK


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
            return body_schema(post), HTTPStatus.CREATED
        else:
            return {
                       "error": {
                           "message": 'Post not found'
                       }
                   }, HTTPStatus.NOT_FOUND

    @auth.login_required
    def get(self, id):
        try:
            post = Post.query.filter_by(id=id).first()
            return body_schema(post), HTTPStatus.OK
        except Exception as e:
            return {
                       "error": {
                           "message": 'Post not found'
                       }
                   }, HTTPStatus.NOT_FOUND

    @auth.login_required
    def delete(self, id):
        post = Post.query.filter(Post.id == id).first()
        if post is not None:
            Post.query.filter(Post.id == id).delete()
            db.session.commit()
            return {"success": True}, HTTPStatus.OK
        else:
            return {
                       "error": {
                           "message": "Post not found"
                       }
                   }, HTTPStatus.NOT_FOUND


class UserPost(Resource):
    @auth.login_required
    def get(self, userId):
        """viewing posts of a specific user"""
        if Post.query.filter(Post.userId == userId).count():
            posts = Post.query.filter(Post.userId == userId)
            js = schema(posts)
            return {'message': 'Success', 'data': js}, HTTPStatus.OK
        else:
            return {'message': 'Posts not found', 'data': {}}, HTTPStatus.NOT_FOUND

    @auth.login_required
    def delete(self, userId):
        """delete specific user posts"""
        if Post.query.filter(Post.userId == userId).count():
            Post.query.filter(Post.userId == userId).delete()
            db.session.commit()
            return '', HTTPStatus.NO_CONTENT
        else:
            return {'message': 'User posts not found', 'data': {}}, HTTPStatus.NOT_FOUND


class Author(Resource):
    @auth.login_required
    def get(self, id):
        """found author of the post by post id"""
        user = User.query.join(User.posts, aliased=True) \
            .filter_by(id=id)

        js = schema_users(user)

        return {'message': 'Success', 'data': js}, HTTPStatus.OK
