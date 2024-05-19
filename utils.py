import datetime

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_time(time_str):
    return datetime.datetime.strptime(time_str, "%H:%M:%S").time()
