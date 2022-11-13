import logging

from fastapi import APIRouter, Depends, HTTPException, status
from rss.reader.db.repository import Repository

from rss.reader.domain.user import User, UserList
from rss.reader.injections.repo import db_repo
from rss.reader.models.not_found import NotFound


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=UserList)
def get_users(repo: Repository = Depends(db_repo)):
    return UserList(users=repo.user.get_all())


@router.get('/{id}', response_model=User,
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def get_user(id: str, repo: Repository = Depends(db_repo)):
    db_user = repo.user.get(query={'_id': id})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id "{id}" not found')
    return db_user
