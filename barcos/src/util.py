from datetime import datetime


def get_year_from_month(month):
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    if current_month == int(month):
        return current_year

    month_string = str(current_year) + "-" + str(month)
    monthTime = datetime.strptime(month_string, "%Y-%m")

    delta = monthTime - now
    delta = delta.total_seconds()

    if delta >= 0:
        return current_year
    else:
        return current_year + 1
