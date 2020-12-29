import json
from botler.utils import read_json_data_files

budget = 29


# read the budget
# def read_budget():
"""
In this function we are going to load our current budget using the API of YNAB
It will return the budget in the variable budget
"""
#   budget = currentbudgetfromAPI
#    return budget


def job_picker(joblist, budget):
    """Search the joblist to find which jobs are doable budjet wise

    Args:
        joblist (dictionary): A dictionary of all the possible jobs including their costs and preperation time
        budget (integer): The amount of money saved for jobs

    Returns:
        list : List of jobs which are doable
                Jobname
                preperation effort
                costs
    """
    # create an empthy lists with the jobs
    possible_jobs = []
    # iterate through the joblist
    for key in joblist.keys():
        jobcost = joblist[key]["costs"]
        # seek the jobs which are doable within the budget
        if jobcost <= budget:
            possible_job = {
                "name": key,
                "preperation_effort": joblist[key]["preperationeffort"],
                "cost": jobcost,
            }
            # add them to the list
            possible_jobs = possible_jobs + [possible_job]
    return possible_jobs


def job_dreamer(joblist, budget):
    """Search the joblist to find which jobs are almost doable budjet wise

    Args:
        joblist (dictionary): A dictionary of all the possible jobs including their costs and preperation time
        budget (integer): The amount of money saved for jobs

    Returns:
        list : List of jobs which are doable in the near future
                job
                preperation effort
                costs
    """
    # create an empthy lists with the jobs
    possible_jobs = []
    # iterate through the joblist
    for key in joblist.keys():
        jobcost = joblist[key]["costs"]
        # seek the jobs with budgets that are almost doable
        if jobcost > budget and jobcost < budget + 50:
            possible_job = {
                "name": key,
                "preperation_effort": joblist[key]["preperationeffort"],
                "cost": jobcost,
            }
            # add them to the list
            possible_jobs = possible_jobs + [possible_job]
    return possible_jobs


if __name__ == "__main__":
    # execute functions
    c = read_json_data_files(path="data/handymans_joblist.json")
    d = job_picker(c, budget)
    e = job_dreamer(c, budget)
    print(d)
    print("almost there ")
    print(e)