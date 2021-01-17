import datetime
import json
from datetime import date
from utils import read_csv_data_calendar
from paths import calendar_path


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

    today = date.today()
    jolly_good_fellows = calendar[calendar["birthday"].dt.month == today.month][
        calendar["birthday"].dt.day == today.day
    ]
    jolly_good_fellows["age"] = today.year - jolly_good_fellows["birthday"].dt.year
    jolly_good_fellows = jolly_good_fellows[["name", "birthday", "nickname", "age"]]
    return jolly_good_fellows


# write function

## mutatie functies

# email api


if __name__ == "__main__":
    # execute functions
    c = read_csv_data_calendar(path=calendar_path)
    b = birthday_is_today(c)
    print(b)
