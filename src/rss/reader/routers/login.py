import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from rss.reader.auth.pwd import verify_user_pwd
from rss.reader.auth.token import create_token
from rss.reader.db.repository import Repository
from rss.reader.domain.user import UserWithPassword
from rss.reader.injections.repo import db_repo
from rss.reader.models.auth import AuthToken, Unauthorized


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/', response_model=AuthToken,
             responses={status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized}})
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          repo: Repository = Depends(db_repo)):
    not_authorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail='Invalid email or password.')
    db_user = repo.user.get(query={'email': form_data.username},
                            return_password=True)
    if not db_user:
        raise not_authorized
    user = UserWithPassword(**db_user)
    if not verify_user_pwd(form_data.password, user.password):
        raise not_authorized

    # token content below is open but could be
    # encrypted to ensure higher application security
    return create_token({
        'user': {
            'id': user.id,
            'name': user.name
        }
    })
