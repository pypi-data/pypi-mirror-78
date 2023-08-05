""" Additional utility functions """
import csv
from pkg_resources import resource_filename, resource_exists


def read_common_mistakes():
    """
    Read the common mistakes database

    Returns:
        Dict: Dict with keys as the words and value as correction
    """
    filename = "resources/common_mistakes.csv"
    mistakes={}
    if resource_exists(__name__, filename):
        mistakes_filename = resource_filename(__name__, filename)
    else:
        raise ValueError("Correction database {} not found ".format(filename))
    with open(mistakes_filename, newline="") as mistakes_file:
        reader = csv.DictReader(mistakes_file, delimiter=",")
        for row in reader:
            mistakes[row['word']]=row['correct']
    return mistakes
