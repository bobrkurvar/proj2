from datetime import date
import logging

def to_date(str_data : str) -> date | None:
    try:
        day, mnt, year = (int(d) for d in str_data.split('.'))
    except ValueError:
        return None
    return date(year=year, month=mnt, day=day)

def to_date_dict(str_data: str) -> dict[str, int] | None:
    try:
        day, mnt, year = (int(d) for d in str_data.split('.'))
    except ValueError:
        return None
    return dict(day=day, month=mnt, year=year)
