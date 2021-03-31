import json
from http import HTTPStatus


def test_auth_hello_success(client):
    response = client.get('api/v1/auth',
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.OK
    assert json_response['result']['message'] == 'Hello, User!'


def test_auth_hello_unauth(client):
    response = client.get('api/v1/auth')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_auth_create_success(client):
    data = {'username': 'username', 'password': 'password'}
    response = client.post('api/v1/auth',
                           data=data,
                           headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.CREATED
    assert json_response['result']['token']


def test_auth_create_422_error(client):
    data = {'username': 'username'}
    response = client.post('api/v1/auth',
                           data=data,
                           headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert json_response['error']


def test_auth_create_unauth(client):
    data = {'username': 'username', 'password': 'password'}
    response = client.post('api/v1/auth', data=data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'
