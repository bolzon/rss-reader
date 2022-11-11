from fastapi.testclient import TestClient

from rss.reader.main import app

cli = TestClient(app)


def test_signup():
    cli.post('/signup', data={})
