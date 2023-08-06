from datetime import date, time, datetime, timedelta

MARCH = 3


def to_financial_year_month_string(now: date):
    if now.month > MARCH:
        year = f'{now.year}-{str(now.year + 1)[-2:]}'
    else:
        year = f'{now.year - 1}-{str(now.year)[-2:]}'

    if now.month < 10:
        month = f'0{now.month}'
    else:
        month = str(now.month)

    return f'{year}-{month}'


def time_to_seconds(t: time):
    return t.hour * 3600 + t.minute * 60 + t.second


def is_saturday(now):
    return now.weekday() == 5


def next_working_day(now: datetime):
    """
    returns next working day.
    :param now:
    :return:
    """
    # if it is saturday, return monday
    if is_saturday(now):
        return now + timedelta(days=2)

    return now + timedelta(days=1)


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
