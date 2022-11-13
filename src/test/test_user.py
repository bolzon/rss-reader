import json

import pytest

from fastapi import status
from fastapi.testclient import TestClient

from rss.reader.main import main
from utils import random_string


app = main()
cli = TestClient(app)
user_pwd = random_string()


@pytest.fixture(scope='module')
def new_user():
    user = {
        'name': 'John Doe',
        'email': f'{random_string(5)}@doe.com',
        'password': user_pwd
    }
    response = cli.post('/signup', json=user, allow_redirects=True)
    return user | response.json()


@pytest.fixture(scope='module')
def token(new_user):
    user = {
        'username': new_user['email'],
        'password': new_user['password']
    }
    response = cli.post('/login', data=user, allow_redirects=True)
    return json.loads(response.content)


@pytest.fixture(scope='module')
def auth_header(token):
    token_type = token['token_type']
    access_token = token['access_token']
    return {'authorization': f'{token_type} {access_token}'}


def test_user_same_as_logged(new_user, auth_header):
    response = cli.get('/user', headers=auth_header)
    assert response.status_code == status.HTTP_200_OK
    json_user = response.json()
    assert all([json_user[k] == new_user[k] for k in ['name', 'email']])
