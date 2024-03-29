import logging

from collections import OrderedDict
from typing import Any, Union

import requests
import xmltodict

from dateutil.parser import parse

from rss.reader.domain.rss_item import RssItem, RssItemList


logger = logging.getLogger(__name__)


def get_json_feed_from_url(url: str) -> Union[OrderedDict[str, Any], None]:
    '''Requests RSS url and returns XML content as JSON (dict).'''
    res = requests.get(url, allow_redirects=True, timeout=20)
    content_type = res.headers.get('content-type', '').lower()
    if content_type.find('xml') < 0:
        logger.debug('Invalid content type for URL: %s (%s)',
                     url, content_type)
        return None
    return xmltodict.parse(res.content)


def load_feed(rss_data: dict[str, Any]) -> dict[str, Any]:
    '''Loads feed info from RSS and return dict with those info.'''
    json_feed = {}
    channel = rss_data.get('rss', {}).get('channel', {})
    if not channel:
        return None
    json_feed['title'] = channel.get('title')
    json_feed['link'] = channel.get('link')
    json_feed['description'] = channel.get('description')
    return json_feed


def load_items(rss_data: dict[str, Any], feed_id: str, user_id: str) -> RssItemList:
    '''Loads items from RSS and return list of dict representing them.'''
    item_list = RssItemList()
    if channel := rss_data.get('rss', {}).get('channel', {}):
        for channel_item in channel.get('item', []):
            pub_date = channel_item.get('pubDate')
            parsed_pub_date = parse(pub_date)
            if parsed_pub_date:
                pub_date = parsed_pub_date.isoformat()
            item_list.items.append(RssItem(
                user_id=user_id,
                feed_id=feed_id,
                title=channel_item.get('title'),
                link=channel_item.get('link'),
                description=channel_item.get('description'),
                pub_date=pub_date
            ))
    return item_list
