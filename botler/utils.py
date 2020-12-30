import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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