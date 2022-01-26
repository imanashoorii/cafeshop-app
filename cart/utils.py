from datetime import date, datetime,timezone
import jdatetime


def toJalaliDateTime(d, time=True):
    if isinstance(d, date) and not isinstance(d, datetime):
        d = datetime(d.year, d.month, d.day)
    if d == None:
        return '-'
    if time == True:
        return jdatetime.datetime.fromgregorian(datetime=d.replace(tzinfo=timezone.utc)).strftime("%Y/%m/%d-%H:%M:%S")
    else:
        return jdatetime.datetime.fromgregorian(datetime=d.replace(tzinfo=timezone.utc)).strftime("%Y/%m/%d")
