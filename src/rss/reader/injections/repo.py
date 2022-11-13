import logging

from typing import Generator

from rss.reader.db.repository import Repository, RepositoryFactory


logger = logging.getLogger(__name__)


def db_repo() -> Generator[Repository, None, None]:
    repo: Repository = RepositoryFactory.create()
    try:
        yield repo
    except Exception as e:
        logger.error(e)
    finally:
        repo.close()
