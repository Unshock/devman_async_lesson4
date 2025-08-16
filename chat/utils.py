from datetime import datetime


def get_formatted_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")
