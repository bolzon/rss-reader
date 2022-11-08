import logging

from fastapi import APIRouter, HTTPException, Request, status

from rss.reader.db.repository.user import UserRepository
from rss.reader.domain.user import User, UserList
from rss.reader.models.not_found import NotFound


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=UserList)
def get_users(request: Request):
    user_repo: UserRepository = request.app.repository.user
    return UserList(users=user_repo.get_all())


@router.get('/{id}', response_model=User,
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def get_user(request: Request, id: str):
    user_repo: UserRepository = request.app.repository.user
    db_user = user_repo.get(filter={'_id': id})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id "{id}" not found'
        )
    return User(**db_user)
