import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status

from rss.reader.db.repository import Repository
from rss.reader.domain.user import User
from rss.reader.injections.repo import db_repo


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=User)
def get_logged_user(request: Request, repo: Repository = Depends(db_repo)):
    db_user = repo.user.get(query={'_id': request.user.id})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id "{request.user.id}" not found')
    return db_user
