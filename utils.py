import aocd
import os
from private import session
import csv


def get_data(day=None, year=None):
    filename = os.path.join('data', f'{year}_{day}.txt')
    if not os.path.isfile(filename):
        data = aocd.get_data(session, day, year)
        with open(filename, 'w') as file:
            file.write(data)
    else:
        with open(filename, 'r') as file:
            data = file.read()

    return data


def submit(answer, day=None, year=None, part=None):
    aocd.submit(answer=answer, part=part, day=day, year=year, session=session,
                reopen=False, quiet=False)
