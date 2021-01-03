from flask import Flask, render_template, request

from birthday_calendar import birthday_is_today
from guest_list import making_a_guestlist, toomuchdays
from job_list import budget, job_picker
from paths import calendar_path, job_path, guest_list_path
from utils import read_csv_data_calendar, read_json_data_files, read_csv_data_files
import pandas as pd

# create a Flask object: a web application
app = Flask(__name__)

# Flask use annotations (starting with the at '@') to connect a URL to a function.
# Here we tells Python to execute hello_world() each time the URL / is called.
@app.route("/")
def make_a_message():
    a = read_csv_data_calendar(calendar_path)
    birthday_frame = birthday_is_today(a)
    if birthday_frame.shape[0] == 0:

        No_one = {"No": [], "birthday": [], "today": []}
        birthdays = pd.DataFrame(No_one)
    # else:
    #     # convert the list into a string
    #     birthdays = birthday_frame
    # c = read_json_data_files(job_path)
    # d = job_picker(c, budget, "affordable")
    # if not d:
    #     jobs = "There's a time to spent money and a time to save money, now is the time to save \n"
    # else:
    #     jobs = " ".join([str(elem) for elem in d])
    # e = job_picker(c, budget, "almost")
    # dream_jobs = " ".join([str(elem) for elem in e])
    # message = birthdays + "\n" + jobs + "\n" + dream_jobs
    return birthdays


@app.route("/hello")
def hello():

    a = read_csv_data_calendar(calendar_path)
    birthday_frame = birthday_is_today(a)
    birthday_frame = birthday_frame[["name", "nickname", "age"]]
    if birthday_frame.shape[0] == 0:
        No_one = {"No": [], "birthday": [], "today": []}
        birthdays = pd.DataFrame(No_one)
    #
    else:
        # convert the list into a string
        birthdays = birthday_frame

    # print(f'[birthdays.to_html(classes="data")]: {[birthdays.to_html(classes="data")]}')
    # print(f"birthdays.columns.values: {birthdays.columns.values}")
    # a = read_json_data_files(calendar_path)
    # birthday_list = birthday_is_today(a)
    # if not birthday_list:
    #     birthdays = "no birthdays today"
    # else:
    #     # convert the list into a string
    #     birthdays = " ".join([str(elem) for elem in birthday_list])
    # read the joblist
    complete_joblist = read_csv_data_files(job_path)
    # See if there are afforable jobs
    affordable_joblist = job_picker(complete_joblist, budget, "affordable")
    if affordable_joblist.shape[0] == 0:
        jobs = "There's a time to spent money and a time to save money, now is the time to save \n"
    else:
        jobs = affordable_joblist
    # if the budget is almost afoordable, pick a dreamjob
    dream_jobs = job_picker(complete_joblist, budget, "almost")

    # adding guests to the list
    loadguests = read_csv_data_files(guest_list_path)
    guests = making_a_guestlist(loadguests, toomuchdays)

    return render_template(
        "hello.html",
        table_bday=[
            birthdays.to_html(classes="data", index=False),
        ],
        table_jobs=[jobs.to_html(index=False)],
        table_drjobs=[dream_jobs.to_html(index=False)],
        # birthdays=birthdays,
        table_guests=[guests.to_html(index=False)],
    )


# This if condition is equivalent to the main() function.
# We tells Python to start our web application.
if __name__ == "__main__":
    app.run(host="0.0.0.0")
