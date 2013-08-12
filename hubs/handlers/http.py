"Handles fetching data over HTTP(S) or FTP"

import os
import logging
import requests
from requests.exceptions import Timeout, ConnectionError

logger = logging.getLogger('hubs')


def check(source):
    """Checks if source is a valid URL."""
    request = requests.PreparedRequest()
    try:
        request.prepare_url(source, None)
    except Exception as e:
        return False
    return True


def writer(target, response):
    for chunk in response:
        target.write(chunk)


def handle(url, timeout = None, **kwargs):
    try:
        response = requests.get(url, stream=True, timeout=timeout)
    except Timeout:
        logger.error('HTTP request timed out', extra={
            'url': url,
            'timeout': timeout
        })
        return
    except ConnectionError as e:
        logger.error('HTTP connection error', extra={
            'url': url
        })
        return

    # TODO handle 202 Accepted, poll until finished
    if response.status_code != 200:
        logger.error('HTTP response not OK', extra={
            'url': url,
            'status_code': response.status_code,
            'reason': response.reason
        })
        return

    if 'name' not in kwargs:
        kwargs.setdefault('name', os.path.basename(url))

    kwargs.setdefault('source', url)

    from hubs.models import Stream
    stream = Stream(**kwargs)
    stream.write(writer, response)
    return stream
