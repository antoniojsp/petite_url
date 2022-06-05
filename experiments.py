import datetime

def expiration_time():
    current_time = datetime.datetime.now()
    time_change = datetime.timedelta(minutes=10)
    new_time = current_time + time_change

    return new_time