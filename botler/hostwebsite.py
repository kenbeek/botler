from flask import Flask, render_template, request

from birthday_calendar import birthday_is_today
from job_list import budget, job_picker
from utils import read_json_data_files
from paths import calendar_path, job_path

# create a Flask object: a web application
app = Flask(__name__)

# Flask use annotations (starting with the at '@') to connect a URL to a function.
# Here we tells Python to execute hello_world() each time the URL / is called.
@app.route("/")
def make_a_message():
    a = read_json_data_files(calendar_path)
    birthday_list = birthday_is_today(a)
    if not birthday_list:
        birthdays = "no birthdays today"
    else:
        # convert the list into a string
        birthdays = " ".join([str(elem) for elem in birthday_list])
    c = read_json_data_files(job_path)
    d = job_picker(c, budget, "affordable")
    if not d:
        jobs = "There's a time to spent money and a time to save money, now is the time to save \n"
    else:
        jobs = " ".join([str(elem) for elem in d])
    e = job_picker(c, budget, "almost")
    dream_jobs = " ".join([str(elem) for elem in e])
    message = birthdays + "\n" + jobs + "\n" + dream_jobs
    return message


@app.route("/hello")
def hello():
    a = read_json_data_files(calendar_path)
    birthday_list = birthday_is_today(a)
    if not birthday_list:
        birthdays = "no birthdays today"
    else:
        # convert the list into a string
        birthdays = " ".join([str(elem) for elem in birthday_list])
    c = read_json_data_files(job_path)
    d = job_picker(c, budget, "affordable")
    if not d:
        jobs = "There's a time to spent money and a time to save money, now is the time to save \n"
    else:
        jobs = " ".join([str(elem) for elem in d])
    e = job_picker(c, budget, "almost")
    dream_jobs = " ".join([str(elem) for elem in e])
    name = birthdays + "\n" + jobs + "\n" + dream_jobs
    return render_template(
        "hello.html",
        dreamjobs=dream_jobs,
        jobs=jobs,
        birthdays=birthdays,
    )


# This if condition is equivalent to the main() function.
# We tells Python to start our web application.
if __name__ == "__main__":
    app.run(host="0.0.0.0")
