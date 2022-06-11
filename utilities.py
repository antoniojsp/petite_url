import configparser
from datetime import datetime
import requests
from random import randrange


def is_url_alive(url: str) -> bool:
    try:
        result = requests.get(url).status_code == 200
    except requests.exceptions.RequestException as e:
        result = False

    return result


def generate_random_hash(size: int) -> str:
    """
    Number of combinations is 62**size
    i.e. if size is 6 then there are combinations 56,800,235,584
    i.e. if size is 7 then there are 3,521,614,606,208 combinations
    """
    hash_result = []
    alphanumeric = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for hash_char_position in range(0, size):
        random_char = randrange(0, 62)
        hash_result.append(alphanumeric[random_char])

    return "".join(hash_result)


def is_expired(time: str) -> bool:
    if time is None:
        return False

    adjusted_time_format = time[:-8]
    pattern_time_format = "%Y-%m-%dT%H:%M"
    current_time = datetime.utcnow()
    expiration_date = datetime.strptime(adjusted_time_format, pattern_time_format)

    return current_time > expiration_date
