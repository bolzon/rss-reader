import logging

from fastapi import APIRouter, HTTPException, Request, status

from rss.reader.domain.user import User, UserList
from rss.reader.models.not_found import NotFound


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=UserList)
def find_users(request: Request):
    return UserList(users=list(
        request.app.col_users.find(
            projection={'password': False},
            limit=20
        )
    ))


@router.get('/{id}', response_model=User,
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def find_user(id: str, request: Request):
    user = request.app.col_users.find_one(
        filter={'_id': id},
        projection={'password': False}
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id "{id}" not found'
        )
    return user
