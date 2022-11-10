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

## Install and run

Application uses MongoDB and Redis to store data and control processing workflows.

If you don't have those tools in your local environment, you can
easily run those on a docker container before you start the application.

```sh
$ docker run -d --rm --network host mongo
$ docker run -d --rm --network host redis
```

### Docker container

Go to `src/` folder and create the updated `requirements.txt` file.

```sh
$ pipenv lock -r > requirements.txt
```

Build the docker image.

```sh
$ docker build -t sendcloud/rss-reader:latest .
```

Run the container.

```sh
$ docker run -it --rm --name rss-reader --network host sendcloud/rss-reader:latest
```

To run the application in background, remove `-it` and add `-d` (detached) arg from the command line above.

### Local dev mode

Go to `src/` folder and install project dependencies.

```sh
$ pipenv install
```

Run the application.

```sh
$ pipenv run app
```

Server URL:
- https://127.0.0.1:8000/

Docs URL (OpenAPI):
  - https://127.0.0.1:8000/docs

## Pylint

Static code analysis is made by [pylint](https://pylint.pycqa.org/).

```sh
$ pipenv run lint
```

## PEP 8

PEP 8 style conventions is checked by [pycodestyle](https://github.com/PyCQA/pycodestyle).

```sh
$ pipenv run pep8
```
