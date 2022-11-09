import logging

from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder

from rss.reader.auth.pwd import encrypt_user_pwd
from rss.reader.db.repository.user import UserRepository
from rss.reader.domain.user import User, UserWithPassword
from rss.reader.models.user import SignupUser


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
def signup(request: Request, user: SignupUser):
    user.password = encrypt_user_pwd(user.password)
    user_repo: UserRepository = request.app.repository.user
    domain_user = UserWithPassword(**jsonable_encoder(user))
    db_user = user_repo.create(jsonable_encoder(domain_user))
    logger.debug('User created: %s', db_user)
    return db_user
