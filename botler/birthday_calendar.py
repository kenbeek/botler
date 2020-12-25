import datetime
import json
from datetime import date


## database
# read function
def read_birthday_calendar():
    """Reads in the data from birthday_calendar.json and returns a dictionary with people and their birthdays

    Returns:
        Dictionary : The complete birthday calendar
    """
    with open("data/birthday_calendar.json", "r+") as f:
        calendar = json.load(f)
    return calendar


def birthday_is_today(calendar):
    """Filters the people whose birthday is today out of the calendar

    Arg
        calendar (dictionary): dictionary of people and their birthdays

    Returns:
        list : List of people whose birthday is today (jolly good fellows)
    """
    jolly_good_fellows = []
    today = date.today()
    for key in calendar.keys():
        birthday = datetime.datetime.strptime(calendar[key]["birthday"], "%d-%m-%Y")
        if birthday.day == today.day and birthday.month == today.month:
            print(key)
            jolly_good_fellow = {
                "name": key,
                "age": today.year - birthday.year,
                "primary_contact": calendar[key]["primary_contact"],
            }
            if c[key]["nickname"] != "None":
                jolly_good_fellow["nickname"] = calendar[key]["nickname"]
            jolly_good_fellows = jolly_good_fellows + [jolly_good_fellow]

    return jolly_good_fellows


# write function

## mutatie functies

# email api


if __name__ == "__main__":
    c = read_birthday_calendar()
    b = birthday_is_today(c)
    print(b)