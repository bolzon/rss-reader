import logging

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

from rss.reader.models.auth import AuthToken, Login, Unauthorized


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/', response_model=AuthToken,
             responses={status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized}})
def login(request: Request, login_data: Login):
    if login_data.email == 'alex@bolzon.com' and login_data.pwd == 'bla':
        return AuthToken(token='fake_token')
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid email or password.'
    )
