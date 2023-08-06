from datetime import datetime, timedelta
from typing import Optional, Dict, List, Optional, Union


def get_start_date(days: int) -> str:
    return str(datetime.today().date() - timedelta(days=days))


def get_today() -> str:
    return str(datetime.today().date() + timedelta(days=1))


def days_last_util(days: int) -> Dict[str, str]:
    startDate = get_start_date(days)
    endDate = get_today()
    return {"startDate": startDate, "endDate": endDate}


def create_date(year: str = None, month: str = None) -> str:
    if year and month:
        return f"{year}-{month}-01"
    if year:
        return f"{year}-01-01"
    if month:
        return f"{datetime.now().year}-{month}-01"
    else:
        return f"{datetime.now().year}-01-01"


def create_date_range(
    days: Optional[int] = None, start: Optional[str] = None, end: Optional[str] = None
) -> List[Union[str, datetime]]:

    if start and end:
        day_diff = (
            datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")
        ).days

        dates = [
            (datetime.strptime(end, "%Y-%m-%d") - timedelta(days=x)).strftime(
                "%Y-%m-%d"
            )
            for x in range(abs(day_diff))
        ]

        for date in dates:
            yield date

    else:
        return [
            (datetime.today().date() - timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range(days)
        ]

