import logging
from threading import Thread
from . import files, path, http, request, default

__all__ = ('put',)

logger = logging.getLogger('hubs')

handlers = (
    request,
    files,
    path,
    http,
    default,
)

class HandlerThread(Thread):
    def __init__(self, handle, source, save, **kwargs):
        self.handle = handle
        self.source = source
        self.save = save
        self.kwargs = kwargs
        super(HandlerThread, self).__init__()

    def run(self):
        streams = self.handle(self.source, **self.kwargs)
        if streams is None:
            return

        if self.save:
            if not isinstance(streams, (list, tuple)):
                streams = [streams]
            for s in streams:
                try:
                    s.save()
                except Exception as e:
                    logger.exception('Error saving stream')
                    continue

        if len(streams) == 1:
            return streams[0]
        return streams


def put(source, save = True, async = False, **kwargs):
    "Shortcut for handling a stream."
    for handler in handlers:
        if handler.check(source):
            thread = HandlerThread(handler.handle, source, save=save, **kwargs)
            if async:
                thread.start()
                return thread
            return thread.run()

    raise ValueError('No valid handler could be determined for source')
