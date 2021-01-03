from utils import read_json_data_files, loaddatafromspreadsheet
from datetime import date, datetime, timedelta

# Threshold for how many days should have past before adding someone to the contactlist
toomuchdays = 500


def loadgoogledata():
    """This function load the data from a google spreadsheet
    Returns:
        a List: Containing the data loaded from the google doc sheet.
    """
    # the key of the googleguestlist file
    key = "1afaA80jq-x1098R0svhcUiMpAykcPqWnUy0tcRFhrG0"
    # use the function in utils to load data
    mydata = loaddatafromspreadsheet(key)
    return mydata


def making_a_guestlist(mydata, toomuchdays):
    """Makes a guestlist with friends and family that we need to call ordered by priority

    Args:
        mydata (list): containing all our the friends and relative
        toomuchdays (int): the amount of days before friends anr relatives appear on the list

    Returns:
        dictionary: An dictoriary with relatives and friend that we need to reach inclucinding their name and priamry contact
    """
    # the inviationdictionairy which we are going to make
    guests_list = []

    # For each item in mydata
    key = 0
    while key < len(mydata):
        # see how many days have passed since the last day
        last_date = mydata[key]["last_day_seen"]
        days_passed = countingdays(last_date)
        # when there have been passed toomuchdays add the person the the invitation dictionary
        if days_passed > toomuchdays:
            guest = {
                "name": mydata[key]["name"],
                "primary_contact": mydata[key]["primary_contact"],
                "rank": days_passed * mydata[key]["priority"],
                "dayspassed": days_passed,
                "priority": mydata[key]["priority"],
            }
            # add them to the dictionary
            guests_list = guests_list + [guest]
        key = key + 1
    # order the list by rank
    guests_list.sort(reverse=True, key=sortingout)
    # print(guests_list)

    # delete the information in the dictionary about the rank, priority and the days that have been passed
    del_key = 0
    for del_key in range(len(guests_list)):
        del guests_list[del_key]["rank"]
        del guests_list[del_key]["priority"]
        del guests_list[del_key]["dayspassed"]
    return guests_list


def sortingout(e):
    """
    To be honest I do not know exactly why this is here, but it works ;)
    """
    return e["rank"]


def countingdays(d0):
    """Counts have many days have passed since a given date (d0)

    Args:
        d0 string: A string describing how many days have passed

    Returns:
        int: A number which is the amount of days that has been passed since the given date
    """
    date_format = "%d-%m-%Y"
    # See what day it is today
    today = datetime.today()
    # Format the given date
    a = datetime.strptime(d0, date_format)
    # calculate the difference between the two dates
    delta = today - a
    return delta.days


if __name__ == "__main__":
    a = loadgoogledata()
    b = making_a_guestlist(a, toomuchdays)
    print("an ordered list of relatives to be invited")
    print(b)
