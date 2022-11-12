# RSS Reader

API motivated by a Sendcloud assessment.

## Tech stack

- Python 3.9 + FastAPI + pipenv
- OAuth2 authentication with user/password
- Docker container ready
- MongoDB as domain storage
- Redis as message broker (for background async tasks)

## Env vars

| Variable | Description | Example |
|:---------|:------------|:--------|
| JWT_SECRET | Secret to encrypt user passwords. | 26faa9...58d95d |
| MONGO_URL | Database url. | mongodb://127.0.0.1:21017 |
| MONGO_DB_NAME | Database name. | rss_reader |
| TOKEN_EXPIRATION_MIN | Token expiration time in minutes. | 15 |

JWT_SECRET can be randomly generated with openssl.

```sh
$ openssl rand -hex 32
```

> **Application loads env vars from a `.env` file in `src/` folder.**

## Install and run

Application and its dependencies run in containers, use docker-compose to execute altogether.

First go to `src/` folder and create an updated `requirements.txt` file.

```sh
$ pipenv lock -r > requirements.txt
```

Build and run.

```sh
$ docker-compose build
$ docker-compose up -d
```

## Dev mode

Go to `src/` folder, install dev deps and run.

```sh
$ pipenv install --dev
$ pipenv run app
```

Server URL:
- https://127.0.0.1:8000/

Docs URL (OpenAPI):
  - https://127.0.0.1:8000/docs


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
