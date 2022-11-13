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


def test_login_ok(new_user):
    user = {
        'username': new_user['email'],
        'password': new_user['password']
    }
    response = cli.post('/login', data=user, allow_redirects=True)
    assert response.status_code == status.HTTP_200_OK


def test_login_invalid():
    invalid_user = {
        'user': 'John',
        'pwd': 'superstrong123'
    }
    response = cli.post('/login', data=invalid_user, allow_redirects=True)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_unauthorized(new_user):
    user = {
        'username': new_user['email'],
        'password': 'invalidpassword'
    }
    response = cli.post('/login', data=user, allow_redirects=True)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
