import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from db.setup import db as database


app = create_app(os.getenv('config', 'config.DevelopmentConfig'))
migrate = Migrate(app, database)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
