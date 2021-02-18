from utils import get_data, submit
import re

data = get_data(4, 2020)
data = data.replace('\n\n', 'seperator')
data = data.replace('\n', ' ')

data = data.split('seperator')

people = []
pattern = r'([a-z]*?):([^ ]*?)(?= |$)'
for line in data:
    person = dict()
    for match in re.finditer(pattern, line):
        person[match[1]] = match[2]
    people.append(person)


def get_a(people):
    count = 0
    for person in people:
        if len([key for key in person if key != 'cid']) == 7:
            count += 1
    return count


def byr_test(value):
    pattern = r'\d{4}'
    return re.fullmatch(pattern, value) and (1920 <= int(value) <= 2002)


def iyr_test(value):
    pattern = r'\d{4}'
    return re.fullmatch(pattern, value) and (2010 <= int(value) <= 2020)


def eyr_test(value):
    pattern = r'\d{4}'
    return re.fullmatch(pattern, value) and (2020 <= int(value) <= 2030)


def hgt_test(value):
    pattern = r'(\d*?)((?:cm)|(?:in))'
    match = re.fullmatch(pattern, value)
    if match is None:
        return False
    elif match[2] == 'cm':
        return (150 <= int(match[1]) <= 193)
    elif match[2] == 'in':
        return (59 <= int(match[1]) <= 76)


def hcl_test(value):
    pattern = r'#[0-9a-f]{6}'
    return bool(re.fullmatch(pattern, value))


def ecl_test(value):
    return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def pid_test(value):
    pattern = r'[0-9]{9}'
    return bool(re.fullmatch(pattern, value))


def get_b(people):
    rules = {
        'byr': byr_test,
        'iyr': iyr_test,
        'eyr': eyr_test,
        'hgt': hgt_test,
        'hcl': hcl_test,
        'ecl': ecl_test,
        'pid': pid_test,
    }
    count = 0
    for person in people:
        if not len([key for key in person if key != 'cid']) == 7:
            continue
        valid = True
        for key, value in person.items():
            if (test := rules.get(key)) is not None:
                if not test(value):
                    valid = False
                    continue
        if valid:
            count += 1
    return count


print(get_b(people))
