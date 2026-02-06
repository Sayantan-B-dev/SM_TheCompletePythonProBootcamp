import datetime as dt

def calculate_detailed_age(now: dt.datetime, dob: dt.datetime) -> dict:
    years = now.year - dob.year
    if (now.month, now.day) < (dob.month, dob.day):
        years -= 1

    months = now.month - dob.month
    if now.day < dob.day:
        months -= 1
    if months < 0:
        months += 12

    last_birthday_year = dob.year + years
    last_birthday_month = dob.month + months

    if last_birthday_month > 12:
        last_birthday_month -= 12
        last_birthday_year += 1

    last_birthday = dt.datetime(
        year=last_birthday_year,
        month=last_birthday_month,
        day=dob.day,
        hour=dob.hour,
        minute=dob.minute,
        second=dob.second
    )

    delta = now - last_birthday
    days = delta.days
    seconds_left = delta.seconds

    return {
        "years": years,
        "months": months,
        "days": days,
        "hours": seconds_left // 3600,
        "minutes": (seconds_left % 3600) // 60,
        "seconds": seconds_left % 60
    }
