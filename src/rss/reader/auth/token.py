import logging
import os

from datetime import datetime, timedelta
from typing import Any, Union

from jose import JWTError, jwt
from jose.constants import Algorithms

from rss.reader.models.auth import AuthToken


JWT_ALG = Algorithms.HS256
JWT_SECRET = os.environ['JWT_SECRET']
TOKEN_EXPIRATION_MIN = int(os.getenv('TOKEN_EXPIRATION_MIN', '15'))


logger = logging.getLogger(__name__)


def create_token(data: dict[str, Any], expire_delta: Union[timedelta, None] = None) -> AuthToken:
    if not expire_delta:
        expire_delta = timedelta(minutes=TOKEN_EXPIRATION_MIN)
    data_to_encode = data.copy()
    data_to_encode['exp'] = datetime.utcnow() + expire_delta
    jwt_encoded = jwt.encode(data_to_encode, key=JWT_SECRET, algorithm=JWT_ALG)
    return AuthToken(access_token=jwt_encoded, token_type='bearer')


def check_token(token: str) -> Union[dict[str, Any], None]:
    try:
        return jwt.decode(token=token, key=JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        logger.error('Invalid token: JWTError')
    return None
