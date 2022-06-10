str = '2023-06-10T23:30:00.000Z'
compare = "2022-06-09 20:39:14.054657"
from datetime import datetime


def is_expired(time: str) -> bool:
    current_time = datetime.utcnow()
    print(current_time)
    expiration_date = datetime.strptime(time[:-8], "%Y-%m-%dT%H:%M")
    print(expiration_date)
    return current_time > expiration_date


print(is_expired(str))