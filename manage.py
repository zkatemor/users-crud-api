import os

from dotenv import load_dotenv
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_httpauth import HTTPTokenAuth

from app import create_app, api
import db
from app.controllers.auth_controller import AuthController
from app.controllers.users_controller import UsersController, UsersIndexController

database = db.get_db()

load_dotenv()

app = create_app(os.environ['APP_SETTINGS'])
migrate = Migrate(app, database)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

api.add_resource(UsersController, '/api/v1/users')
api.add_resource(UsersIndexController, '/api/v1/users/<int:id>')

api.add_resource(AuthController, '/api/v1/auth')

if __name__ == '__main__':
    manager.run()
