import json
import logging

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

from rss.reader.domain.rss_feed import RssFeed
from rss.reader.models.not_found import NotFound


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=list[RssFeed])
def list_feeds(request: Request):
    feeds = request.app.col_rss_feeds.find({
        'user_id': 'asd'
    })
    return feeds