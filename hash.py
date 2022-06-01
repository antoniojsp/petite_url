import hashlib


def hash_url(url: str, size = 5) -> hash:
    return hashlib.shake_256(url.encode()).hexdigest(size)

