import logging

from typing import Callable

from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, OperationFailure


logger = logging.getLogger(__name__)


class DbProvider:
    def __init__(self, url: str, dbname: str):
        self.client: MongoClient = MongoClient(url)
        self.db = self.client.get_database(dbname)
        logger.info('Connected to DB: %s (%s)', url, dbname)

    def close(self):
        logger.info('Closing DB connection')
        self.client.close()


class DbTransaction:
    def __init__(self, db_provider: DbProvider, tx: Callable):
        self.db_provider = db_provider
        self.tx = tx

    def execute(self):
        session = self.db_provider.client.start_session()
        db_txctx = DbTransactionContext(self, session)
        try:
            with session.start_transaction():
                self.tx(db_txctx)
                session.commit_transaction()
        except (ConnectionFailure, OperationFailure) as e:
            raise DbTransaction(e)


class DbTransactionContext:
    def __init__(self, db_tx: DbTransaction, session: ClientSession):
        self.db_tx = db_tx
        self.session: ClientSession = session

    def get_collection(self, name: str, db_name: str) -> Collection:
        return self.session.client.get_database(db_name).get_collection(name)


class DbTransactionError(RuntimeError):
    def __init__(self, msg: str, parent_ex: Exception):
        super().__init__(**parent_ex)
