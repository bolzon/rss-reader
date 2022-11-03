import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from rss.reader.auth.provider import create_token, verify_user_pwd
from rss.reader.domain.user import UserWithPassword
from rss.reader.models.auth import AuthToken, Unauthorized


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/', responses={status.HTTP_200_OK: {'model': AuthToken},
                             status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized}})
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserWithPassword(**request.app.col_users.find_one(
        filter={'email': form_data.username}
    ))
    if not user or not verify_user_pwd(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password.'
        )
    return create_token({'id': user.id, 'name': user.name})
