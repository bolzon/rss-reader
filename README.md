# RSS reader (or scraper)

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

Here's the list of things that I'd like to have improved, but couldn't implement due to the tight time.

- **Cache.** To improve the performance of the API requests.
- **Service layer.** That layer would help to abstract a little bit more the logic present in routers.
- **Pagination.** An absolute must have for any API, but once it was not in the requirements, I opted to focus on other things.
- **DB transactions.** I started to implement it, but left the initial code in a separate branch. It certainly must be part of a production-ready system.
- **Events-driven architecture.** That would lead the system to a next level with a little bit more complex architecture, so I decided to go for a monolith for now, once it's a simple application and it was advised to _avoid over-engineering_.
- **More tests.** Tests, such as the application itself, take lots of time to design and implement, but once they are in place, things are way easier to implement as well as the quality of the software is also assured.
- **Documentation.** I'm still trying different options to generate Python documentation, so I don't have a favorite yet, but it's absolutelly something that adds a lot to any maintainable software.

## Final considerations

I'm really glad to be participating of your recruitment process, so I've tried to use as much known concepts I could to show you a little bit of my background and the way I'm used to code. That involves how I organize my code in a repo, how I think both, functional and OOP programming are equally useful when it comes to using it right, how generators and list comprehensions are powerful and lastly, how I write readme files.

I truly hope that I could have reached the minumum requirements of the test and we could follow to the next step. If not, I had a great time participating of this process even though and hope to see you soon any time in the future.

## About

- Author: **Alexandre Bolzon**
- Delivered: **14th November 2022**
- Social: **[abolzon](https://abolzon.com)** | **[github](https://github.com/bolzon/)** | **[linkedin](https://www.linkedin.com/in/alexandrebolzon/)**
