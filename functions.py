import datetime
import re

def validatedate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def isValidTime(time):
    regexPattern = "(1[012]|[1-9]):" + "[0-5][0-9](\\s)" + "?(?i)(am|pm)"
    compiledPattern = re.compile(regexPattern)

    if (time == None):
        raise ValueError("Time specified can't be none")

    try:
        re.search(compiledPattern, time)
    except ValueError:
        raise ValueError("Incorrect time format")