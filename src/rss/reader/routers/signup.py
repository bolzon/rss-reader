import json
import logging

from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder

from rss.reader.auth.pwd import encrypt_user_pwd
from rss.reader.domain.user import User, UserWithPassword


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
def signup(request: Request, user: UserWithPassword):
    user.password = encrypt_user_pwd(user.password)
    json_user = jsonable_encoder(user)
    new_user = request.app.col_users.insert_one(json_user)
    created_user = request.app.col_users.find_one(
        filter={'_id': new_user.inserted_id},
        projection={'password': False}
    )
    logger.debug('User created: %s', json.dumps(created_user))
    return created_user
