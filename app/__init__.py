from flask import Flask
from flask_restful import Api

api = Api()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from db.setup import db
    db.init_app(app)

    api.app = app
    api.authorizations = {
        'apiKey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }
    return app
