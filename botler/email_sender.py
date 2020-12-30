import email
import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

from birthday_calendar import birthday_is_today
from utils import read_json_data_files
from paths import calendar_path, job_path


def load_environment_variables():
    """load variables from .env file and store them in global
    variables"""
    load_dotenv(".env")
    # port for SMTP
    global port
    port = 465
    # sending email address
    global sender_email
    sender_email = os.getenv("SENDER_EMAIL")
    # receiving email address
    global receiver_email
    receiver_email = os.getenv("RECEIVER_EMAIL")
    # password for sender email address
    global password
    password = os.getenv("PASSWORD")


def compose_birthday_message():
    # read in the birthday calendar
    calendar = read_json_data_files(calendar_path)
    # get the people whose birthday is today
    # jgfs = jolly good fellows
    jgfs = birthday_is_today(calendar)
    # make content of email dependent on number of birthdays

    if len(jgfs) == 0:
        subject = "No birthdays today"
        text = "There are no birthdays today."
    elif len(jgfs) == 1:
        # jgfs is in the form of a list. Take the first (and only)
        # element of the list.
        jgf = jgfs[0]
        # combine name and nickname (if it exists) into a handle
        handle = get_handle(jgf)
        # turn age into correct ordinal
        age_ordinal = str(jgf["age"]) + get_number_suffix(jgf["age"])

        # enter the name into the subject
        subject = f"Birthday reminder: {jgf['name']}"
        # enter the name, nickname and age into the message
        text = f"""
Hi,

Don't forget it's {handle}'s {age_ordinal} birthday today.

        """
    elif len(jgfs) > 1:
        # Add names to subject
        names = ", ".join([jgf["name"] for jgf in jgfs])
        subject = f"Birthday reminders: {names}"
        # Create a base message
        text = f"""
Hi,

These people have a birthday today:

"""
        # Add the jolly good fellows to the message
        for jgf in jgfs:
            # combine name and nickname (if it exists) into a handle
            handle = get_handle(jgf)
            # turn age into correct ordinal
            age_ordinal = str(jgf["age"]) + get_number_suffix(jgf["age"])
            message = message + f"""{handle}'s' {age_ordinal} birthday) \n"""

    else:
        # valueerror if none of the above apply
        ValueError: "Impossible value for len(jgfs)"

    # create a MIME object for the email.
    # This ensures we can later switch to HTML emails easily.
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    # turn email text into MIME object
    mime_text = MIMEText(text, "plain")
    # add mime text to mime object
    message.attach(mime_text)
    # return the message, and also the number of birthdays because we
    # want to condition on that later. In the future, it may be worth it
    # to look at the option of not returning anything when len(jgfs) ==
    # 0, since in that case we don't want to send an email anyway.
    return (message, len(jgfs))


def send_email(message, number_of_birthdays):
    """Send an email message if there are >0 birthdays

    Args: message (MIME multipart email): MIME object containing the
        email information
        number_of_birthdays (int): number of birthdays today.
    """
    sender_email = message["From"]
    receiver_email = message["To"]
    # only send an email if there are birthdays today
    if number_of_birthdays > 0:
        context = ssl.create_default_context()

        # send email via smtplib
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())


def get_number_suffix(number):
    """returns the correct suffix to turn a number into an ordinal

    Args:
        number (int): a number

    Returns: string : the ordinal suffix
    """
    if number % 10 == 1:
        return "st"
    elif number % 10 == 2:
        return "nd"
    elif number % 10 == 3:
        return "rd"
    else:
        return "th"


def get_handle(jgf):
    if "nickname" in jgf.keys():
        handle = jgf["name"] + " (" + jgf["nickname"] + ")"
    else:
        handle = jgf["name"]
    return handle


if __name__ == "__main__":
    # execute the functions
    load_environment_variables()
    (message, number_of_birthdays) = compose_birthday_message()
    send_email(message, number_of_birthdays)
