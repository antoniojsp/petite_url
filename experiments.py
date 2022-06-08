from datetime import datetime
from datetime import timedelta


def is_expired(time: str) -> bool:
    if time == "None":
        return False
    current_time = datetime.now()
    expiration_date = datetime.strptime(time, "%Y/%m/%dT%H:%M")

    return current_time > expiration_date

print(is_expired("2022/06/09T02:30"))