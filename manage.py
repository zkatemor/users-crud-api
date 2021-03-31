import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, api
from db.setup import db as database
from app.controllers.auth_controller import AuthController
from app.controllers.users_controller import UsersController, UsersIndexController
from app.controllers.post_controller import PostssController, PostsIndexController


app = create_app(os.getenv('config', 'config.DevelopmentConfig'))
migrate = Migrate(app, database)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

api.add_resource(UsersController, '/api/v1/users')
api.add_resource(UsersIndexController, '/api/v1/users/<int:id>')

api.add_resource(PostssController, '/api/v1/posts')
api.add_resource(PostsIndexController, '/api/v1/posts/<int:id>')

api.add_resource(AuthController, '/api/v1/auth')

if __name__ == '__main__':
    manager.run()
