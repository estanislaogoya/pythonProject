#dates.py

from dateutil.rrule import rrule, DAILY

def getDatesDiff(start, end):
    date_str = []
    for date in rrule(DAILY, dtstart=start, until=end):
        if date.weekday() < 5:
            date_str.append("{y}-{m}-{d}".format(y=date.year,m=date.month,d=date.day))
    return date_str

def set_approach(a,b):
    return list(set(a)-set(b))
