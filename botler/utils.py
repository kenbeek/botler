import json


def read_json_data_files(path):
    """Reads in the data from a json file and returns a
    dictionary with the contents

    Args:
        path (str): the location of the data file on disk.

    Returns:
        Returns: Dictionary : The contents of the file
    """

    with open(path, "r+") as f:
        data = json.load(f)
    return data