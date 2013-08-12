"Handles file upload in a request."

from django.http import HttpRequest
from hubs.utils import request_client_ip
from files import handle as handle_file


def check(source):
    return isinstance(source, HttpRequest)


def handle(request, **kwargs):
    if 'origin' not in kwargs:
        pass

    if 'source' not in kwargs:
        kwargs['source'] = request_client_ip(request)

    streams = []

    for upload in request.FILES.values():
        streams.append(handle_file(upload, **kwargs))
    return streams
