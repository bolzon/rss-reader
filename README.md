# RSS Reader

Application creation was motivated by a SoundCloud assessment.

## Requirements

- Application written in Python 3.9
- Code dependencies managed by [pipenv](https://pipenv.pypa.io/en/latest/)

## Install and run

### Docker

First, go to `src/` folder and create the updated `requirements.txt` file.

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
$ pipenv run uvicorn rss.reader.main:app
```

Server URL
- https://127.0.0.1:8000/

Docs URL (OpenAPI)
  - https://127.0.0.1:8000/redoc

## Pylint

Static code analysis is made by [pylint](https://pylint.pycqa.org/).

## PEP 8

PEP 8 style conventions is checked by [pycodestyle](https://github.com/PyCQA/pycodestyle).