import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import read_json_data_files
from datetime import date


def loadgoogledata():
    gc = gspread.service_account(filename="mycredentials.json")
    gsheet = gc.open_by_key("1afaA80jq-x1098R0svhcUiMpAykcPqWnUy0tcRFhrG0")
    mydata = gsheet.sheet1.get_all_records()
    return mydata


def isKArenhere(mydata):
    key = 0
    while key < len(mydata):
        if mydata[key]["last_day_seen"] == "karen":
            print("karen was here!")
            print("she got an")
            print(mydata[key]["grade"])
            karenstatus = "Karen present"
        else:
            print("no karen")
        key = key + 1
    return karenstatus


def coutingdays():
    d0 = date(2008, 8, 18)
    d1 = date(2008, 9, 26)
    delta = d1 - d0
    print(delta.days)


if __name__ == "__main__":
    a = loadgoogledata()
    b = isKArenhere(a)
    print("What is the status of Karen?")
    print(b)
# print(mydata[0]["name"])
