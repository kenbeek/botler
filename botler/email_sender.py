import os
import smtplib
import ssl

from dotenv import load_dotenv

from birthday_calendar import birthday_is_today, read_birthday_calendar


def load_environment_variables():
    load_dotenv(".env")
    global port
    port = 465
    global sender_email
    sender_email = os.getenv("SENDER_EMAIL")
    global receiver_email
    receiver_email = os.getenv("RECEIVER_EMAIL")
    global password
    password = os.getenv("PASSWORD")


def compose_birthday_message():
    calendar = read_birthday_calendar()
    jgfs = birthday_is_today(calendar)
    if len(jgfs) == 0:
        message = "There are no birthdays today."
    elif len(jgfs) == 1:
        jgf = jgfs[0]
        message = f"""\
Subject: Birthday reminder: {jgf['name']}


Hi,

Don't forget it's {jgf['name']}\'s {('(' + jgf['nickname'] + ') ' ) if ('nickname' in jgf.keys()) else ""}{jgf['age']}\'s birthday today.

        """
    elif len(jgfs) > 1:
        message = f"""
Subject: Birthday reminders: {[jgf['name'] for jgf in jgfs]}


Hi,

These people have a birthday today:

"""

        for jgf in jgfs:
            message = (
                message
                + f"""{jgf['name']} {('(' + jgf['nickname'] + ') ' ) if ('nickname' in jgf.keys()) else ""} ({jgf['age']} years old) \n"""
            )

    else:
        ValueError: "Impossible value for len(jgfs)"

    return (message, len(jgfs))


def send_email(message, sender_email, receiver_email):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


if __name__ == "__main__":
    load_environment_variables()
    (message, number_of_birthdays) = compose_birthday_message()
    if number_of_birthdays > 0:
        send_email(message, sender_email, receiver_email)