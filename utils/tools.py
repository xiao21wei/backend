import re
import string
import random


def valid_username(s):
    if s is None:
        return False
    if 2 <= len(s) <= 12:
        if re.match('^[0-9a-zA-Z_]+$', s[0:]):
            return True
        else:
            return False
    else:
        return False


def valid_password(s):
    if s is None:
        return False
    if 8 <= len(s) <= 18:
        a = 0
        b = 0
        for i in s:
            if i.isalpha():
                a = 1
            if i.isdigit():
                b = 1
        if a + b == 2 and s.isalnum():
            return True
        else:
            return False
    else:
        return False


def random_room():
    random_list = []
    for i in range(16):
        random_list.append(random.choice(string.ascii_uppercase + string.digits))
    return ''.join(random_list)

