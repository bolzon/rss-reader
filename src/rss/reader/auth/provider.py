import json
import logging

from fastapi import HTTPException, Request, status


logger = logging.getLogger(__name__)


def auth_user(request: Request):
    # logger.debug(json.dumps(request.__dict__, indent=2, default=str))
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Access denied'
    )
    request.scope['user'] = 'that is my user'