import requests


def is_url_alive(url: str) -> bool:
    try:
        result = requests.get(url).status_code == 200
    except requests.exceptions.RequestException as e:
        result = False
    return result



