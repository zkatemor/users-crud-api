import json
from http import HTTPStatus


def test_posts_show_success(client):
    response = client.get('api/v1/posts',
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.OK
    assert json_response['result'][0]['title'] == 'test'


def test_posts_show_unauth(client):
    response = client.get('api/v1/posts')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_posts_create_success(client):
    data = {'title': 'create', 'body': 'create',
            'userId': 1}
    response = client.post('api/v1/posts',
                           data=data,
                           headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.CREATED
    assert json_response['result']['title'] == data['title']


def test_posts_create_422_error(client):
    data = {'title': 'create'}
    response = client.post('api/v1/posts',
                           data=data,
                           headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert json_response['error']


def test_posts_create_unauth(client):
    data = {'title': 'create', 'body': 'create',
            'userId': 1}
    response = client.post('api/v1/posts', data=data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_posts_update_success(client):
    data = {'title': 'update', 'body': 'update',
            'userId': 1}
    response = client.put('api/v1/posts/1',
                          data=data,
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.CREATED
    assert json_response['result']['title'] == data['title']


def test_posts_update_unauth(client):
    data = {'title': 'update', 'body': 'update',
            'userId': 1}
    response = client.put('api/v1/posts/1', data=data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_posts_update_404(client):
    data = {'title': 'create', 'body': 'create',
            'userId': 1}
    response = client.put('api/v1/posts/111',
                          data=data,
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_response['error']


def test_posts_delete_success(client):
    response = client.delete('api/v1/posts/1',
                             headers={'Authorization': 'Bearer token'})

    assert response.status_code == HTTPStatus.OK


def test_posts_delete_unauth(client):
    response = client.delete('api/v1/posts/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_posts_delete_404(client):
    response = client.delete('api/v1/posts/111',
                             headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_response['error']


def test_posts_index_success(client):
    response = client.get('api/v1/posts/1',
                          headers={'Authorization': 'Bearer token'})

    assert response.status_code == HTTPStatus.OK


def test_posts_index_unauth(client):
    response = client.get('api/v1/posts/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_posts_get_404(client):
    response = client.get('api/v1/posts/111',
                          headers={'Authorization': 'Bearer token'})
    json_response = json.loads(response.data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_response['error']


def test_author_success(client):
    response = client.get('api/v1/user/post/1',
                          headers={'Authorization': 'Bearer token'})

    assert response.status_code == HTTPStatus.OK


def test_author_unauth(client):
    response = client.get('api/v1/user/post/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_user_posts_success(client):
    response = client.get('api/v1/posts/user/1',
                          headers={'Authorization': 'Bearer token'})

    assert response.status_code == HTTPStatus.OK


def test_user_posts_404(client):
    response = client.get('api/v1/posts/user/11',
                          headers={'Authorization': 'Bearer token'})

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_posts_unauth(client):
    response = client.get('api/v1/posts/user/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'


def test_user_posts_delete_success(client):
    response = client.delete('api/v1/posts/user/1',
                             headers={'Authorization': 'Bearer token'})

    assert response.status_code == 204


def test_user_posts_delete_404(client):
    response = client.get('api/v1/posts/user/11',
                          headers={'Authorization': 'Bearer token'})

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_posts_delete_unauth(client):
    response = client.get('api/v1/posts/user/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == b'Unauthorized Access'
