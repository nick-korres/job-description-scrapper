from datetime import datetime


def convert_string_to_datetime(date_string:str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")

def convert_datetime_to_string(date:datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S.%f")

def days_diff_from_now(date:str) -> int :
    date_obj = convert_string_to_datetime(date)
    now = datetime.now()
    return (now - date_obj).days