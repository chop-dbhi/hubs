import hashlib


def request_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def file_md5(filename, block_size=65536):
    "Computes the MD5 hexdigest of a file."
    md5 = hashlib.md5()

    with open(filename, 'rb') as fin:
        while True:
            data = fin.read(block_size)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()
