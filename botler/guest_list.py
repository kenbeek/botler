from utils import read_csv_data_files
from paths import guest_list_path
from datetime import date, datetime, timedelta

# Threshold for how many days should have past before adding someone to the contactlist
toomuchdays = 500


def making_a_guestlist(mydata, toomuchdays):
    """Makes a guestlist with friends and family that we need to call ordered by priority

    Args:
        mydata (pandas): containing all our the friends and relative
        toomuchdays (int): the amount of days before friends anr relatives appear on the list

    Returns:
        pandas: A panda with relatives and friend that we need to reach inclucinding their name and priamry contact
    """
    # Make a new colum including the amount of days passed since we last invited the friend
    mydata.insert(len(mydata.columns), "days_passed", "")
    mydata["days_passed"] = mydata["last_day_seen"].apply(lambda x: countingdays(x))
    # Filter out the friends that we have recently seen
    filtered_mydata = mydata[mydata["days_passed"] >= toomuchdays]
    # Add a colum with the calculated rank of the friend based on the last day seen and the priority
    filtered_mydata.insert(len(filtered_mydata.columns), "rank", "")
    filtered_mydata["rank"] = (
        filtered_mydata["days_passed"] * filtered_mydata["priority"]
    )
    # Sort the guest_listbased on the priority
    guests_list = filtered_mydata.sort_values(by=["rank"], ascending=False)
    # Remove the priority, rank, last day seen and days passed from the list
    guests_list = guests_list.drop(
        columns=["rank", "priority", "last_day_seen", "days_passed"]
    )
    return guests_list


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
    a = read_csv_data_files(guest_list_path)
    b = making_a_guestlist(a, toomuchdays)
    print("an ordered list of relatives to be invited")
    print(b)
