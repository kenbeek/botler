import json
import os
from datetime import date, timedelta
import datetime
from dotenv import find_dotenv, load_dotenv
from utils import shell_response
from email_sender import load_environment_variables
import pandas as pd


def get_grocery_budget():
    # load the ynab keys from .env file
    dotenv_location = find_dotenv()
    load_dotenv(dotenv_location)
    ynab_key = os.getenv("YNAB_KEY")
    budget_id_gezamenlijk = os.getenv("BUDGET_ID_GEZAMENLIJK")
    category_id_groceries = os.getenv("CATEGORY_ID_GROCERIES")

    # add the key and ID's into the shell command
    grocery_command = f'curl -X GET "https://api.youneedabudget.com/v1/budgets/{budget_id_gezamenlijk}/categories/{category_id_groceries}" -H "accept: application/json" -H "Authorization: Bearer {ynab_key}"'
    # catch the response of the command
    budget = shell_reponse(grocery_command)
    # locate the correct number in the dictionary
    grocery_budget = output_json["data"]["category"]["balance"] / 1000

    return grocery_budget


def count_sundays(start_date, end_date):
    """Count how many sundays are in a given date range
    We count this because weekly grocery shopping should be done on sunday

    Args:
        start_date ([date]): start date of range
        end_date ([date]): end date of range

    Returns:
        [int]: number of sundays in date range
    """
    return sum([x.weekday() == 6 for x in pd.date_range(start_date, end_date).tolist()])


def get_next_payday():
    """Returns the next day when new money will come ine

    Returns:
        [datetime date]: the next payday
    """
    # set a vakue on which day of the month new money arrives
    payday = 25
    # get todays date
    today = date.today()
    # Get the date of the next 25th. This is different when we are in
    #  the first 25 days of the month from when we are past the 25th
    if today.day < payday:
        next_payday = datetime.datetime.strptime(
            # if the current day of the month is lower than 25, it's
            # the 25th of this month
            f"{payday}-{today.month}-{today.year}",
            "%d-%m-%Y",
        )
    else:
        next_payday = datetime.datetime.strptime(
            # if the current day of the month is higher than 25, it's
            # the 25th of next month
            f"{payday}-{today.month+1}-{today.year}",
            "%d-%m-%Y",
        )
    return next_payday


def budget_for_this_week():
    # set a value for the weekly grocery budget
    budget_per_week = 72
    # get today's date
    today = date.today()
    # get the date of the next payday
    end_of_current_period = get_next_payday() - timedelta(days=1)
    # read how much money is left in the grocery category on ynab
    grocery_budget = get_grocery_budget()
    # count how many sundays are left until the next payday
    sundays = count_sundays(today, end_of_current_period)
    # calculate how much money we have left for this week
    return grocery_budget - sundays * budget_per_week


if __name__ == "__main__":
    print(f"We have €{budget_for_this_week()} left for this week.")
