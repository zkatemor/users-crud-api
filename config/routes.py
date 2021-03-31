from app.controllers.auth_controller import AuthController
from app.controllers.post_controller import PostssController, PostsIndexController
from app.controllers.users_controller import UsersController, UsersIndexController


def register_routes(api):
    api.add_resource(UsersController, '/api/v1/users')
    api.add_resource(UsersIndexController, '/api/v1/users/<int:id>')

    api.add_resource(PostssController, '/api/v1/posts')
    api.add_resource(PostsIndexController, '/api/v1/posts/<int:id>')

    api.add_resource(AuthController, '/api/v1/auth')
