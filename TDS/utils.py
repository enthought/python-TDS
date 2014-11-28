import re


def convert(name):
    """Convert a CamelCase identifier to lower_case.

    Taken from http://stackoverflow.com/questions/1175208/
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
