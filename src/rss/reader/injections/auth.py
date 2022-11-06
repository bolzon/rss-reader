import logging

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from rss.reader.auth.token import check_token
from rss.reader.models.auth import AuthUser


logger = logging.getLogger(__name__)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/login')


def auth_user(request: Request, token: str = Depends(oauth2_bearer)):
    if not (decoded_token := check_token(token)) or 'user' not in decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    request.scope['user'] = AuthUser(**decoded_token['user'])
