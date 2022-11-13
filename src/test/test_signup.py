import pytest

from fastapi import status
from fastapi.testclient import TestClient

from rss.reader.main import main
from utils import random_string


app = main()
cli = TestClient(app)


@pytest.fixture(scope='module')
def user():
    return {
        'name': 'John Doe',
        'email': f'{random_string(5)}@doe.com',
        'password': random_string()
    }


@pytest.fixture(scope='module')
def signup_res(user):
    response = cli.post('/signup', json=user, allow_redirects=True)
    return response


def test_signup_bad_request(user):
    user = user.copy()
    user['email'] = 'invalidemail'
    response = cli.post('/signup', json=user, allow_redirects=True)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_signup_ok(signup_res):
    assert signup_res.status_code == status.HTTP_201_CREATED


def test_signup_user_created(user, signup_res):
    new_user = signup_res.json()
    assert 'password' not in new_user
    assert all([new_user[k] == user[k] for k in ['name', 'email']])
