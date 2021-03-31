from http import HTTPStatus


def test_users_show(client):
    response = client.get('api/v1/users')
    assert response.status_code == HTTPStatus.OK
