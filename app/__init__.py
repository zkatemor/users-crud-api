from flask import Flask
from flask_restful import Api

from config.routes import register_routes
from models.post import Post
from models.token import Token
from models.user import User


def create_app(config='config.ProductionConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from db.setup import db
    db.init_app(app)

    _ = (User, Post, Token)

    api = Api(app)
    register_routes(api)

    api.app = app
    api.authorizations = {
        'apiKey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }

    return app
