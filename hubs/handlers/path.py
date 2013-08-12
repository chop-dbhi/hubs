"Handles referencing or copying files by path."

import os
from files import handle as handle_file


def check(source):
    return os.path.exists(source)


def handle(path, copy = False, **kwargs):
    if copy:
        with open(path, 'rb') as source:
            return handle_file(source, binary=True, **kwargs)

    if 'name' not in kwargs:
        kwargs['name'] = os.path.basename(path)

    kwargs['source'] = path
    kwargs['content_path'] = path

    from hubs.models import Stream
    stream = Stream(**kwargs)
    return stream
