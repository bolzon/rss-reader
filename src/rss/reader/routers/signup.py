import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from rss.reader.auth.pwd import encrypt_user_pwd
from rss.reader.db.repository import Repository
from rss.reader.domain.user import User, UserWithPassword
from rss.reader.injections.repo import db_repo
from rss.reader.models.user import SignupUser, UserAlreadyExists


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User,
             responses={status.HTTP_400_BAD_REQUEST: {'model': UserAlreadyExists}})
def signup(user: SignupUser, repo: Repository = Depends(db_repo)):
    if repo.user.get(query={'email': user.email}) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User already exists')
    user.password = encrypt_user_pwd(user.password)
    domain_user = UserWithPassword(**jsonable_encoder(user))
    db_user = repo.user.create(jsonable_encoder(domain_user))
    logger.debug('User created: %s', db_user)
    return db_user
