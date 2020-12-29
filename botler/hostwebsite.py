# import the class Flask from the flask package
from flask import Flask, request

# import the birthdays
from birthday_calendar import birthday_is_today, read_birthday_calendar

# import the jobs
from job_list import budget, job_picker, job_dreamer, read_joblist

# create a Flask object: a web application
app = Flask(__name__)

# Flask use annotations (starting with the at '@') to connect a URL to a function.
# Here we tells Python to execute hello_world() each time the URL / is called.
@app.route("/")
def make_a_message():
    a = read_birthday_calendar()
    birthday_list = birthday_is_today(a)
    if not birthday_list:
        birthdays = "no birthdays today"
    else:
        # convert the list into a string
        birthdays = " ".join([str(elem) for elem in birthday_list])
    c = read_joblist()
    d = job_picker(c, budget)
    if not d:
        jobs = "There's a time to spent money and a time to save money, now is the time to save \n"
    else:
        jobs = " ".join([str(elem) for elem in d])
    e = job_dreamer(c, budget)
    dream_jobs = " ".join([str(elem) for elem in e])
    message = birthdays + "\n" + jobs + "\n" + dream_jobs
    return message


# This if condition is equivalent to the main() function.
# We tells Python to start our web application.
if __name__ == "__main__":
    app.run(host="0.0.0.0")
