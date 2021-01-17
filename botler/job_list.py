import json
from utils import read_json_data_files, read_csv_data_files
from paths import job_path

budget = 29


# read the budget
# def read_budget():
"""
In this function we are going to load our current budget using the API of YNAB
It will return the budget in the variable budget
"""
#   budget = currentbudgetfromAPI
#    return budget


def job_picker(joblist, budget, mode):
    """Search the joblist to find which jobs are doable budjet wise

    Args:
        joblist (pandas): A table of all the possible jobs
            including their costs and preperation time
        budget (integer): The amount of money saved for jobs
        mode : discribing if we are looking for projects with costs within the budget or almost within the budget

    Returns:
        list : List of jobs which are doable
                Jobname
                preperation effort
                costs
    """

    # if modus is affordable
    if mode == "affordable":
        possible_jobs = joblist[joblist["costs"] <= budget]
    # if modus is almost
    elif mode == "almost":
        possible_jobs = joblist[joblist["costs"] >= budget][
            joblist["costs"] < budget + 50
        ]
    else:
        raise ValueError("mode must be affordable or almost")
    return possible_jobs


if __name__ == "__main__":
    # execute functions
    c = read_csv_data_files(path=job_path)
    d = job_picker(c, budget, "affordable")
    e = job_picker(c, budget, "almost")
    print(d)
    print("almost there ")
    print(e)