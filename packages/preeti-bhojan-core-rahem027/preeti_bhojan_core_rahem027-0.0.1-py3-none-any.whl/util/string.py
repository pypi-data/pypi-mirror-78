import re


def is_alphanumeric_underscore_or_space(string):
    return re.search(r'^[\w\s]+$', string) is not None
