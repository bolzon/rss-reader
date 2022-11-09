# RSS Reader

API motivated by a Sendcloud assessment.

## Tech stack

- Python 3.9 + FastAPI + pipenv
- OAuth2 authentication
- Docker container ready
- MongoDB as database

## Env vars

| Var | Description | Example |
|-----|-------------|---------|
| JWT_SECRET | Secret to encrypt user passwords. | 26faa9...58d95d |
| MONGO_URL | Database url. | mongodb://127.0.0.1:21017 |
| MONGO_DB_NAME | Database name. | rss_reader |

JWT_SECRET can be randomly generated with openssl.

```sh
$ openssl rand -hex 32
```

## Install and run

Application uses MongoDB to store data, so if you don't have a running MongoDB instance in your environment,
you can run it on a docker container before you start the application.

```sh
$ docker run -d --rm --network host mongo
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
