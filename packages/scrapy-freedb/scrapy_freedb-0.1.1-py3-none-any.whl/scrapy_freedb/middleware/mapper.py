import hashlib

def url_sha256(request):
    url = request.url
    hash = hashlib.sha256()
    hash.update(url.encode())
    return hash.hexdigest()


def url_sha1(request):
    url = request.url
    hash = hashlib.sha1()
    hash.update(url.encode())
    return hash.hexdigest()

def url(request):
    return request.url
