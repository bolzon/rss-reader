# RSS Reader (or scraper)

"Simple RSS scraper application which saves RSS feeds to a database and lets a user view and manage feeds they’ve added to the system through an API. Think of Google Feedburner as an example."

(from the [requirements](./reqs/RSS_reader.pdf))

## Stack

- Python 3.9 + FastAPI + pipenv
- OAuth2 authentication with user/password
- Docker container to run app and its deps
- MongoDB as the domain storage and tasks control
- Dramatiq to run the background workers
- Redis as dramatiq message broker
- Apscheduler for the task scheduling
- Pytest for integration tests

## Env vars

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

> **Application loads env vars from a `.env` file in `src/` folder.**

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

## Development mode

Run mongo and redis in background.

```sh
$ docker-compose up -d mongo redis
```

Go to `src/` folder, install all deps and run.

```sh
$ pipenv install --dev
$ pipenv run workers
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

## Improvements

Here's the list of things that I'd like to have improved, but couldn't implement due to the tight time.

- **DB transactions.** I started to implement it, but left the initial code in a separate branch. It certainly must be part of a production-ready system.
- **Service layer.** That layer would help to abstract a little bit more the logic present in routers.
- **Cache.** To improve the performance of the API requests.
- **Pagination.** A must have for a scalable API, but couldn't be implemented due to the tight time.
- **Events-driven architecture.** That would lead system to a little bit more complex architecture with many other points of concern, so I decided to go for a monolith for now, once it's a simple application.
- **More tests.** Tests, such as the application itself, take lots of time to design and implement, but once they are in place, things are way easier to implement as well as the quality of the software that can also be assured.
