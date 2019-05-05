import datetime
import re
import speech

DAYS_IN_A_WEEK = 7
WEEKS_IN_A_YEAR = 52
LARGE_NUMBER_DAYS = 3650


def sunday_from(amazon_date, future_days_go_back_year_threshold=LARGE_NUMBER_DAYS):
    # Returns a datetime object for the given Amazon.DATE
    if re.match(r"20\d\d-\d\d-\d\d", amazon_date):
        date = datetime.datetime.strptime(amazon_date, "%Y-%m-%d").date()
        if (date - datetime.date.today()).days > future_days_go_back_year_threshold:
            date = datetime.date(date.year - 1, date.month, date.day)
        if date.weekday() == 6:
            return date
        else:
            raise RuntimeError(speech.DATE_IS_NOT_A_SUNDAY)
    elif re.match(r"20\d\d-W\d\d-WE", amazon_date):
        amazon_date = amazon_date[:-3]

    if re.match(r"20\d\d-W\d\d", amazon_date):
        original_year = int(amazon_date[:4])
        original_week = int(amazon_date[6:8])

        today_year = datetime.date.today().year
        today_week = datetime.date.today().isocalendar()[1]
        future_weeks_threshold = future_days_go_back_year_threshold / DAYS_IN_A_WEEK

        weeks_difference = ((original_year - today_year) * WEEKS_IN_A_YEAR) + \
                           (original_week - today_week)

        if weeks_difference > future_weeks_threshold:
            amazon_date = str(original_year - 1) + amazon_date[4:]
        # Convert week to Sunday
        return datetime.datetime.strptime(
            amazon_date + "-0", "%Y-W%U-%w").date()
    else:
        print(amazon_date)
        return None


def is_not_in_future(date):
    return date <= date.today()


def date_from_ccm_xml_text(text):
    return datetime.datetime.strptime(text[:-6], "%a, %d %b %Y %H:%M:%S").date()
