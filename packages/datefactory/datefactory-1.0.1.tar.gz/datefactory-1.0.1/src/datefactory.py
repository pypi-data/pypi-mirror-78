from calendar import monthrange
import datetime

def isWeekendDay(day):
    """Function Description
    Tells if the day is a Saturday or Sunday

    Parameters:
    datetime object day

    Returns:
    boolean True if the param is Sat. or Sun; otherwise False

    """    
    if day.weekday() in weekendDays:
        return True

    return False

def isMonday(day):
    """Function Description
    Tells if the day is a Monday

    Parameters:
    datetime object day

    Returns:
    boolean True if the param is a Monday; otherwise False

    """        
    if day.weekday() == 0: #0 is Monday
        return True

    return False

def isFriday(day):
    """Function Description
    Tells if the day is a Friday

    Parameters:
    datetime object day

    Returns:
    boolean True if the param is a Friday; otherwise False

    """            
    if day.weekday() == 4: #0 is Friday
        return True

    return False

def isLastDayOfMonth(day):
    """Function Description
    Tells if the day is the last day of the month e.g. 31/Jan or 29/Feb in a leap year

    Parameters:
    datetime object day

    Returns:
    boolean True if the param is the last day of the month; otherwise False

    """
    
    daysThisMonth = monthrange(day.year, day.month)

    if day.day == daysThisMonth[1]:
        return True
    
    return False

def lastDayOfMonth(day):
    """Function Description
    Calculates the date of the last day of the month e.g. 31/Jan or 29/Feb in a leap year

    Parameters:
    datetime object day

    Returns:
    Datetime object which is the last day of the month of the arg passed in

    """

    daysThisMonth = monthrange(day.year, day.month)
    return createDatetimeObj(daysThisMonth[1], day.month, day.year)

def createDatetimeObj(day, month, year, hour=0, min=0, sec=0):
    """Function Description
    Creates a datetime object

    Parameters:
    day - the numerical day 
    month - the numerical month 
    year - the numerical year 
    hour - the numerical hour (default 0)
    min - the numerical minute  (default 0)
    sec - the numerical second  (default 0)

    Returns:
    datetime object

    """
    
    date_time_str = str(year) + '-' + str(month) + '-' + str(day) + ' '
    date_time_str = date_time_str + str(hour) + ':' + str(min) + ':' + str(sec) + '.123456'
    
    return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

def addDaysToDate(date, numberOfDays):
    """Function Description
    Increments (or decrements) the date by a given number of days

    Parameters:
    datetime object - day
    int - number of days (can be negative)

    Returns:
    A new datetime object with the inc/dec applied

    """    
    return date + datetime.timedelta(days=numberOfDays)


