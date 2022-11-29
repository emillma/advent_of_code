# from utils import submit, get_data

from utils import get_data, submit

data = get_data(1, 2019)
data = [int(i) for i in data.splitlines()]


def foo(number):
    return number//3 - 2


svar_a = sum(foo(i) for i in data)


def bar(number):
    total = foo(number)
    previous = foo(total)
    while previous > 0:
        total += previous
        previous = foo(previous)
    return total


svar_b = sum(bar(i) for i in data)
