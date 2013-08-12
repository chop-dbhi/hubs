"Handles file-like objects."

import os
from django.utils import timezone
from django.core.files.base import File

CHUNK_SIZE = 64 * 1024


def check(source):
    return hasattr(source, 'read')


def writer(dest, source):
    while True:
        chunk = source.read(CHUNK_SIZE)
        if chunk == '':
            break
        dest.write(chunk)


def handle(fin, binary = False, **kwargs):
    if hasattr(fin, 'mode') and 'b' in fin.mode:
        binary = True

    if hasattr(fin, 'name'):
        kwargs.setdefault('name', os.path.basename(fin.name))
        kwargs.setdefault('source', fin.name)

    from hubs.models import Stream
    stream = Stream(**kwargs)
    stream.write(writer, fin, binary=binary)
    return stream
