# import datetime
from datetime import datetime


def expiration_time(time: str):
    current_time = datetime.now()
    expiration_date = datetime.strptime(time, "%Y-%m-%dT%H:%M")
    return current_time > expiration_date


print(expiration_time("2018-06-12T19:30"))
