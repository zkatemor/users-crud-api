import json
from http import HTTPStatus


def test_users_show_success(client):
    response = client.get('api/v1/users',
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.OK
    assert json_response['result'][0]['username'] == 'test'


def test_users_show_unauth(client):
    response = client.get('api/v1/users')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_users_create_success(client):
    data = {'username': 'create', 'first_name': 'create',
            'last_name': 'create', 'is_active': False}
    response = client.post('api/v1/users',
                           data=data,
                           headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.CREATED
    assert json_response['result']['username'] == data['username']


def test_users_create_422_error(client):
    data = {'first_name': 'create',
            'last_name': 'create', 'is_active': False}
    response = client.post('api/v1/users',
                           data=data,
                           headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert json_response['error']


def test_users_create_unauth(client):
    data = {'username': 'create', 'first_name': 'create',
            'last_name': 'create', 'is_active': False}
    response = client.post('api/v1/users', data=data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_users_update_success(client):
    data = {'username': 'update', 'first_name': 'update',
            'last_name': 'update', 'is_active': False}
    response = client.put('api/v1/users/1',
                          data=data,
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.CREATED
    assert json_response['result']['username'] == data['username']


def test_users_update_unauth(client):
    data = {'username': 'create', 'first_name': 'create',
            'last_name': 'create', 'is_active': False}
    response = client.put('api/v1/users/1', data=data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_users_update_404(client):
    data = {'username': 'update', 'first_name': 'update',
            'last_name': 'update', 'is_active': False}
    response = client.put('api/v1/users/111',
                          data=data,
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_response['error']


def test_users_delete_success(client):
    response = client.delete('api/v1/users/2',
                             headers={'Authorization': 'Bearer token'})

    assert response.status_code == HTTPStatus.OK


def test_users_delete_unauth(client):
    response = client.delete('api/v1/users/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_users_delete_404(client):
    response = client.delete('api/v1/users/111',
                             headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_response['error']


def test_users_index_success(client):
    response = client.get('api/v1/users/2',
                          headers={'Authorization': 'Bearer token'})

    assert response.status_code == HTTPStatus.OK


def test_users_index_unauth(client):
    response = client.get('api/v1/users/2')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_users_get_404(client):
    response = client.get('api/v1/users/111',
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_response['error']
