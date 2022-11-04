# RSS Reader

API motivated by a Sendcloud assessment.

## Tech stack

- Implemented in Python 3.9 with FastAPI
- OAuth2 authentication
- Code dependencies managed by [pipenv](https://pipenv.pypa.io/en/latest/)
- Docker container ready
- MongoDB as database

## Env vars

| Var | Description | Example |
|-----|-------------|---------|
| JWT_SECRET | Secret to encrypt user passwords. | 26faa9...58d95d |
| MONGO_URL | MongoDB url. | mongodb://0.0.0.0:21017 |
| MONGO_DB_NAME | Database name. | rss_reader |

JWT_SECRET can be randomly generated with openssl.

```sh
$ openssl rand -hex 32
```

## Install and run

### Docker

Go to `src/` folder and create the updated `requirements.txt` file.

```sh
$ pipenv lock -r > requirements.txt
```

Build the docker image.

```sh
$ docker build -t sendcloud/rss-reader:latest .
```

Finally, run the container.

```sh
$ docker run -it --rm --name rss-reader --network host sendcloud/rss-reader:latest
```

To run the application in background, remove `-it` and add `-d` (detached) arg from the command line above.

### Locally (development mode)

Project dependencies are managed by [pipenv](https://pipenv.pypa.io/en/latest/).

Go to `src/` folder.

Install project dependencies.

```sh
$ pipenv install
```

Run the application.

```sh
$ pipenv run uvicorn rss.reader.main:app --reload
```

Server URL
- https://127.0.0.1:8000/

Docs URL (OpenAPI)
  - https://127.0.0.1:8000/docs

## Pylint

Static code analysis is made by [pylint](https://pylint.pycqa.org/).

## PEP 8

PEP 8 style conventions is checked by [pycodestyle](https://github.com/PyCQA/pycodestyle).