from datetime import datetime
from datetime import timedelta


def record_time(time, utc: int) -> str:
    if time == "None":
        return False
    expiration_date = datetime.strptime(time, "%Y-%m-%dT%H:%M")

    delta = expiration_date + timedelta(minutes=utc)

    date_time = delta.strftime("%Y/%m/%dT%H:%M")
    return date_time




print(record_time("2022-06-07T06:20", 420))