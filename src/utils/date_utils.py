import datetime
import re

DAYS_IN_A_WEEK = 7
WEEKS_IN_A_YEAR = 52
LARGE_NUMBER_DAYS = 3650


def sunday_from(raw_amazon_date: str, future_days_go_back_year_threshold: int = LARGE_NUMBER_DAYS) -> datetime.date:
    if re.match(r"20\d\d-\d\d-\d\d", raw_amazon_date):
        date: datetime.date = datetime.datetime.strptime(raw_amazon_date, "%Y-%m-%d").date()
        if (date - datetime.date.today()).days > future_days_go_back_year_threshold:
            date = datetime.date(date.year - 1, date.month, date.day)
        weekday: int = date.weekday()
        if weekday == 6:
            return date
        elif date.weekday() < 3:
            return date - datetime.timedelta(1 + weekday)
        else:
            return date + datetime.timedelta(6 - weekday)
    amazon_date: str = raw_amazon_date[:-3] if re.match(r"20\d\d-W\d\d-WE", raw_amazon_date) else raw_amazon_date

    if re.match(r"20\d\d-W\d\d", amazon_date):
        original_year: int = int(amazon_date[:4])
        original_week: int = int(amazon_date[6:8])

        today_year: int = datetime.date.today().year
        today_week: int = datetime.date.today().isocalendar()[1]
        future_weeks_threshold: int = future_days_go_back_year_threshold // DAYS_IN_A_WEEK

        weeks_difference: int = ((original_year - today_year) * WEEKS_IN_A_YEAR) + (original_week - today_week)
        if weeks_difference > future_weeks_threshold:
            amazon_date = str(original_year - 1) + amazon_date[4:]
        # Convert week to Sunday
        return datetime.datetime.strptime(amazon_date + "-0", "%Y-W%U-%w").date()
    else:
        raise ValueError(f"Invalid date: {amazon_date}")


def is_not_in_future(date: datetime.date) -> bool:
    return date <= date.today()


def date_from_ccm_xml_text(text: str) -> datetime.date:
    return datetime.datetime.strptime(text[:-6], "%a, %d %b %Y %H:%M:%S").date()
