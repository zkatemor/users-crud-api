import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import create_app
from db.setup import db as _db
from models.post import Post
from models.token import Token
from models.user import User


@pytest.fixture
def app():
    # создание тестового приложения
    app = create_app('config.TestingConfig')

    app_ctx = app.app_context()
    app_ctx.push()

    # на время тестовой сессии создаем базу данных с данными
    # и очищаем ее после тестовой сессии
    with app.app_context():
        _db.create_all()
        _add_test_data()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# добавление в тестовую бд тестовых данныъ
def _add_test_data():
    session = None
    try:
        engine = create_engine(os.environ['TEST_DATABASE_URL'], echo=False)

        session = Session(bind=engine)

        user = User(username='test',
                    first_name='Test',
                    last_name='Test',
                    is_active=True)
        session.add(user)
        session.commit()
        print("first new user created successfully.")

        user1 = User(username='test1',
                     first_name='Test1',
                     last_name='Test1',
                     is_active=True)
        session.add(user1)
        session.commit()
        print("second new user created successfully.")

        post = Post(title='test',
                    body='Test',
                    userId=1)
        session.add(post)
        session.commit()
        print("new post created successfully.")

        token = Token(user='User',
                      password='qwerty',
                      token='token')
        session.add(token)
        session.commit()
        print("new token created successfully.")
    except Exception as error:
        print(error)
    finally:
        if session is not None:
            session.close()
            print('Database connection closed.')
