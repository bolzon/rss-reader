# RSS reader

API to manage RSS feeds.

- subscribe users
- follow/unfollow feeds
- mark feed items as read/unread

Background (scheduled) worker to fetch feeds items.

## Stack

- Python 3.9 + FastAPI + pipenv
- OAuth2 authentication with user/password
- Docker container to run app and its deps
- MongoDB as the domain storage and tasks control
- Dramatiq to run the background workers
- Redis as dramatiq message broker
- Apscheduler for the task scheduling
- Pytest for integration tests

## Environment

Application loads env vars from a `.env` file in `src/` folder.

| Variable | Description | Example |
|:---------|:------------|:--------|
| FEEDS_UPDATE_INTERVAL | Interval in minutes to update feeds. | 15 |
| JWT_SECRET | Secret to encrypt user passwords. | 26faa9...58d95d |
| MONGO_URL | Database url. | mongodb://127.0.0.1:21017 |
| MONGO_DB_NAME | Database name. | rss_reader |
| TOKEN_EXPIRATION_MIN | Token expiration time in minutes. | 15 |

JWT_SECRET can be randomly generated with openssl.

```sh
$ openssl rand -hex 32
```

## Install and run

Use docker-compose to execute application and its dependencies altogether.

First go to `src/` folder and create an updated `requirements.txt` file.

```sh
$ pipenv lock -r > requirements.txt
```

Build and run.

```sh
$ docker-compose build
$ docker-compose up -d
```

Server URL:
- http://127.0.0.1:8000/

Docs URL (OpenAPI):
- http://127.0.0.1:8000/docs

## Development mode

Run mongo and redis in background.

```sh
$ docker-compose up -d mongo redis
```

Go to `src/` folder, install all deps and run.

```sh
# on terminal 1

$ pipenv install --dev
$ pipenv run workers

# on terminal 2

$ pipenv run app
```

## Test

Go to `src/` folder, install dev deps and run.

```sh
$ pipenv install --dev
$ pipenv run test
```

## Pylint

Static code analysis is made by [pylint](https://pylint.pycqa.org/).

```sh
$ pipenv run lint
```

## Improvements

List of things that can be improved:

- **Cache.** To improve the performance of the API requests.
- **Service layer.** That layer would help to abstract a little bit more the logic present in routers.
- **Pagination.** To go through items listed from the database.
- **DB transactions.** Started to implement it, but left the initial code in a separate branch.
- **Events-driven architecture.** Might be useful, but will add substantial complexity.
- **More tests.** Especially for the background workers.
- **Documentation.** Code and system documentation.
