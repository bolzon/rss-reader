import base64
import json
import logging

from typing import Any

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from rss.reader.models.auth import AuthToken, AuthUser


logger = logging.getLogger(__name__)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/login')


def encrypt_user_pwd(pwd: str) -> str:
    return base64.b64encode(pwd.encode('utf8')).decode('utf8')


def verify_user_pwd(pwd: str, encrypted_pwd: str) -> str:
    return encrypt_user_pwd(pwd) == encrypted_pwd


def create_token(data: dict[str, Any]) -> AuthToken:
    b64data = base64.b64encode(json.dumps(data).encode('utf8')).decode('utf8')
    return AuthToken(access_token=b64data, token_type='bearer')


def check_token(token: str) -> bool:
    return True


def decode_token(token: str) -> AuthUser:
    logger.debug('Decoding token: %s', token)
    return AuthUser(id='123', name='fake user')


def auth_user(request: Request, token: str = Depends(oauth2_bearer)):
    # logger.debug(json.dumps(request.__dict__, indent=2, default=str))
    decoded_token = decode_token(token)
    if not check_token(decoded_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    request.scope['user'] = decoded_token
    logger.debug('Token: %s', token)
