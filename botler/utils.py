import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
from flask import render_template


def read_json_data_files(path):
    """Reads in the data from a json file and returns a
    dictionary with the contents

    Args:
        path (str): the location of the data file on disk.

    Returns:
        Returns: Dictionary : The contents of the file
    """

    with open(path, "r+") as f:
        data = json.load(f)
    return data


def read_csv_data_calendar(path):
    """Reads in the calendar csv file and formats the dates

    Args:
        path (str): the path where the file is stored

    Returns:
        Pandas DataFrame: DataFrame of birthdays
    """
    data = pd.read_csv(path)
    # hier roepen we fornat_date aan
    data["birthday"] = data["birthday"].apply(lambda x: format_date(x))
    return data


def read_csv_data_files(path):
    """Reads in the calendar csv file and formats the dates

    Args:
        path (str): the path where the file is stored

    Returns:
        Pandas DataFrame: DataFrame of birthdays
    """
    data = pd.read_csv(path)
    return data


def format_date(date):
    try:
        formatted_date = datetime.datetime.strptime(date, "%d-%m-%Y")
    except:
        try:
            formatted_date = datetime.datetime.strptime(date, "%d/%m/%Y")
        except:
            raise ValueError("date not in correct format")
    return formatted_date


def loaddatafromspreadsheet(key_googledocsheet):
    """This function load the data from a google spreadsheet
    Returns:
        a List: Containing the data loaded from the google doc sheet.
    """
    # Reads the credentials to get access
    gc = gspread.service_account(filename="mycredentials.json")
    # Opens a google sheetfile depending on the key
    gsheet = gc.open_by_key(key_googledocsheet)
    # Saves the data in a list
    mydata = gsheet.sheet1.get_all_records()
    return mydata


if __name__ == "__main__":
    data = read_csv_data_calendar("./data/birthday_calendar.csv")
    print(data)
