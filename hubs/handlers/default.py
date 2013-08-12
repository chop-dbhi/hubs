"Takes an iterator and writes it to the content."

def check(source):
    return True


def writer(dest, content):
    if isinstance(content, basestring):
        dest.write(content)
    else:
        for chunk in content:
            dest.write(chunk)


def handle(content, **kwargs):
    from hubs.models import Stream
    stream = Stream(**kwargs)
    stream.write(writer, content)
    return stream
