from flask_restful import Resource, reqparse

from app.auth.handlers import auth
from models.post import Post
from db.setup import db


def body_schema(post):
    return {"result": {'id': post.id,
                       'title': post.title,
                       'body': post.body,
                       'userId': post.userId}}


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
            return body_schema(post), 201
        except Exception as e:
            return {
                       "error": {
                           "message": str(e)
                       }
                   }, 422

    @auth.login_required
    def get(self):
        query = Post.query.order_by(Post.id).all()
        data = schema(query)
        return data, 200


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
        try:
            title, body, userId = self.update_params()

            post = Post.query.filter(Post.id == id).first()
            if post is not None:
                try:
                    if title:
                        Post.query.filter_by(id=id).update({'title': title})

                    if body:
                        Post.query.filter_by(id=id).update({'body': body})

                    if userId:
                        Post.query.filter_by(id=id).update({'userId': userId})

                    db.session.commit()
                    post = Post.query.filter(Post.id == id).first()

                    db.session.commit()
                    return body_schema(post), 201
                except Exception as e:
                    return {
                               "error": {
                                   "message": str(e)
                               }
                           }, 422
            else:
                return {
                           "error": {
                               "message": 'Post not found'
                           }
                       }, 404

        except Exception as e:
            return {
                       "error": {
                           "message": str(e)
                       }
                   }, 422

    @auth.login_required
    def get(self, id):
        try:
            post = Post.query.filter_by(id=id).first()
            return body_schema(post), 200
        except Exception as e:
            return {
                       "error": {
                           "message": 'Post not found'
                       }
                   }, 404

    @auth.login_required
    def delete(self, id):
        try:
            post = Post.query.filter(Post.id == id).first()
            if post is not None:
                Post.query.filter(Post.id == id).delete()
                db.session.commit()
                return {"success": True}, 200
            else:
                return {
                           "error": {
                               "message": "Post not found"
                           }
                       }, 404
        except Exception as e:
            return {
                       "error": {
                           "message": str(e)
                       }
                   }, 404
