import pytest
import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from rss.reader.main import main

app = main()
cli = TestClient(app)


def random_string(length: int = 10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture(scope='module')
def user():
    return {
        'name': 'John Doe',
        'email': f'{random_string(5)}@doe.com',
        'password': '{random_string()'
    }


@pytest.fixture(scope='module')
def signup_res(user):
    response = cli.post('/signup', json=user, allow_redirects=True)
    return response


def test_signup_status(signup_res):
    assert signup_res.status_code == status.HTTP_201_CREATED


def test_signup_validate_user(user, signup_res):
    new_user = signup_res.json()
    assert 'password' not in new_user
    assert all([new_user[k] == user[k] for k in ['name', 'email']])
