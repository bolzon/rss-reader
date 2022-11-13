from typing import Any


def exclude_none_keys(feed: dict[str, Any]) -> dict[str, Any]:
    '''Returns dict whose values are not None.'''
    return {k: v for k, v in feed.items() if v is not None}


def split_list(the_list: list[Any], items: int = 1000):
    '''Yields successive items-sized chunks from the given list.'''
    for i in range(0, len(the_list), items):
        yield the_list[i:i + items]
