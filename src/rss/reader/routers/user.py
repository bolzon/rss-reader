import json
import logging

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

from rss.reader.domain.user import User
from rss.reader.models.not_found import NotFound


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request: Request, user: User):
    json_user = jsonable_encoder(user)
    new_user = request.app.col_users.insert_one(json_user)
    created_user = request.app.col_users.find_one(
        {'_id': new_user.inserted_id}
    )
    logger.debug('User created: %s', json.dumps(created_user))
    return created_user


@router.get('/{id}', response_model=User,
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def find_user(id: str, request: Request):
    if (user := request.app.col_users.find_one({'_id': id})) is not None:
        logger.debug('User found: %s', json.dumps(user))
        return user
    logger.debug('User not found: %s', id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User with id "{id}" not found'
    )
