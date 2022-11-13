import logging

from typing import Any


logger = logging.getLogger(__name__)


def notify_user_feed_update_failed(user: dict[str, Any], feed: dict[str, Any]):
    user_name = user['name']
    user_email = user['email']
    feed_url = feed['url']

    body = f'''
        Dear {user_name},

        Your feed failed to update:
        {feed_url}

        Please try again at PUT /feed/.

        Cheers,
        RSS Reader
    '''

    send_email(email_from='RSS Reader <rss@reader.com>', email_to=user_email,
               subject='Your feed failed to update', body=body)


def send_email(email_from: str, email_to: str, subject: str, body: str):  # pylint: disable=unused-argument
    # fake email send
    logger.info('Sending email to notify user about feed update failure.')
