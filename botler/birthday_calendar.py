import datetime
import json
from datetime import date


## database
# read function
def read_birthday_calendar(path="data/birthday_calendar.json"):
    """Reads in the data from birthday_calendar.json and returns a
    dictionary with people and their birthdays

    Returns: Dictionary : The complete birthday calendar
    """
    with open(path, "r+") as f:
        calendar = json.load(f)
    return calendar


def birthday_is_today(calendar):
    """Filters the people whose birthday is today out of the calendar

    Arg
        calendar (dictionary): dictionary of people and their birthdays

    Returns:
        list : List of people whose birthday is today (jolly good fellows)
                The objects in the list are dictionaries with the following keys:
                name
                age
                primary_contact
                nickname (may be empty)
    """
    # create an empty list of jolly good fellows
    jolly_good_fellows = []
    today = date.today()
    # check every contact if their birthday is today
    for key in calendar.keys():
        birthday = datetime.datetime.strptime(calendar[key]["birthday"], "%d-%m-%Y")
        if birthday.day == today.day and birthday.month == today.month:
            # if a contact's birthday is today, record the relevant information
            jolly_good_fellow = {
                "name": key,
                "age": today.year - birthday.year,
                "primary_contact": calendar[key]["primary_contact"],
            }
            # If there is a nickname, add it to the list
            if calendar[key]["nickname"] != "None":

                jolly_good_fellow["nickname"] = calendar[key]["nickname"]
            # add them to the list
            jolly_good_fellows = jolly_good_fellows + [jolly_good_fellow]

    return jolly_good_fellows


# write function

## mutatie functies

# email api


if __name__ == "__main__":
    # execute functions
    c = read_birthday_calendar()
    b = birthday_is_today(c)
    print(b)