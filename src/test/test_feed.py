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


@pytest.fixture(scope='module')
def user_id(auth_header):
    response = cli.get('/user', headers=auth_header)
    return response.json()['_id']


def test_feed_list_unauthorized():
    response = cli.get('/feed')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_feed_list_ok(auth_header):
    response = cli.get('/feed', headers=auth_header)
    assert response.status_code == status.HTTP_200_OK


def test_feed_list_feeds(auth_header):
    response = cli.get('/feed', headers=auth_header)
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content)


def test_feed_follow(user_id, auth_header):
    data = {'url': 'http://www.nu.nl/rss/Algemeen'}
    response = cli.post('/feed/follow', json=data, headers=auth_header)
    assert response.status_code == status.HTTP_200_OK

    json_feed = response.json()
    assert all([k in json_feed for k in ['url', 'user_id']])
    assert json_feed['url'].lower() == data['url'].lower()
    assert json_feed['user_id'] == user_id


def test_feed_ufollow(user_id, auth_header):
    data = {'url': 'http://www.nu.nl/rss/Algemeen'}
    response = cli.post('/feed/unfollow', json=data, headers=auth_header)
    assert response.status_code == status.HTTP_200_OK

    json_res = response.json()
    assert 'deleted' in json_res
    assert int(json_res['deleted']) > 0
