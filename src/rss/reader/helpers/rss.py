from dateutil.parser import parse
from typing import Any

from rss.reader.domain.rss_feed import RssFeed
from rss.reader.domain.rss_item import RssItem, RssItemList


def update_feed(rss_data: dict[str, Any], feed: RssFeed):
    channel = rss_data.get('rss', {}).get('channel', {})
    if not channel:
        return None
    feed.title = channel.get('title')
    feed.link = channel.get('link')
    feed.description = channel.get('description')


def get_items(rss_data: dict[str, Any], feed_id: str, user_id: str) -> RssItemList:
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
