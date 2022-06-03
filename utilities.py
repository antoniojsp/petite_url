import hashlib
import urllib.request


def hash_url(url: str, size = 5) -> hash:
    return hashlib.shake_256(url.encode()).hexdigest(size)


def check_url_alive(url: str) -> bool:
    try:
        result = urllib.request.urlopen(url).getcode() == 200
    except (urllib.error.URLError, ValueError) as error:
        result = False

    return result

