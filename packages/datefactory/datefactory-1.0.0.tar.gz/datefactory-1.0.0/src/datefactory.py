from calendar import monthrange
import datetime

def isWeekendDay(day):
    if day.weekday() in weekendDays:
        return True

    return False

def isMonday(day):
    if day.weekday() == 0: #0 is Monday
        return True

    return False

def isFriday(day):
    if day.weekday() == 4: #0 is Friday
        return True

    return False

def isLastDayOfMonth(day):
    daysThisMonth = monthrange(day.year, day.month)

    if day.day == daysThisMonth[1]:
        return True
    
    return False

def lastDayOfMonth(day):
    daysThisMonth = monthrange(day.year, day.month)
    return createDatetimeObj(daysThisMonth[1], day.month, day.year)

def createDatetimeObj(day, month, year, hour=0, min=0, sec=0):
    date_time_str = str(year) + '-' + str(month) + '-' + str(day) + ' '
    date_time_str = date_time_str + str(hour) + ':' + str(min) + ':' + str(sec) + '.123456'
    
    return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

def addDaysToDate(date, numberOfDays):
    return date + datetime.timedelta(days=numberOfDays)


