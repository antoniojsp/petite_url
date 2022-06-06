import datetime
from datetime import datetime


def expiration_time(time: str):
    current_time = datetime.now()
    expiration_date = datetime.strptime(time, "%Y-%m-%d")
    return current_time > expiration_date


print(expiration_time("2022-6-1"))
