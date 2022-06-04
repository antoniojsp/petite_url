import hashlib
import urllib.request
from random import randrange
import configparser


def enviroment_settings(file_name: str) -> dict:
    configurations = configparser.ConfigParser()
    configurations.read(file_name)
    dictionary_secrets = {}

    for i in configurations:
        for j in configurations[i]:
            dictionary_secrets[j] = configurations[i][j]

    return dictionary_secrets


def check_url_alive(url: str) -> bool:
    try:
        result = urllib.request.urlopen(url).getcode() == 200
    except (urllib.error.URLError, ValueError) as error:
        result = False

    return result


def generate_random_hash(size:int) -> str:
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
