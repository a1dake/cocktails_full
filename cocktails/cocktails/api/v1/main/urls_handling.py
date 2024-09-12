import random
from typing import List
import textwrap

from rest_framework.exceptions import ValidationError

VARIES = {
    "1": ['kP5P', 'cq7Z', '2mnZ', 'wwl6'],
    "2": ['YY2d', 'a0sW', 'iW4N', 'kJA2'],
    "3": ['dU6s', 'Mu2C', '3SXF', 'ham3'],
    "4": ['c9dG', 'T5Ls', '5nCE', 'ibw7'],
    "5": ['Pk1C', 'YY1Z', '8sYd', 'lAX5'],
    "6": ['hE4A', 'AV9I', '7Dgr', 'svc4'],
    "7": ['s8aY', 'Bs1s', '1OGq', 'Kls8'],
    "8": ['zX0X', 'JK8s', '6tTw', 'rrR2'],
    "9": ['l3Rq', 'uU4s', '0lMN', 'RTE1'],
    "0": ['B1Bk', 'f3uf', '0Vci', 'iia9']
}


def make_string_link(number: int) -> str:
    keys_to_encode = [letter for letter in str(number)]
    result = ''
    for key in keys_to_encode:
        result += random.choice(VARIES[key])
    if random.choice([True, False]):
        return (result[0:2] + 'G3x6w' + result[2::])[::-1]
    return result[0:2] + 'b2K7a' + result[2::]


def slicer(text: str) -> List:
    return textwrap.wrap(text, 4)


def searcher(slice: str) -> str:
    for key, value in VARIES.items():
        if slice in value:
            return str(key)


def decode_link(string: str) -> int:
    rev_str = string[::-1]
    code = slicer(string[0:2] + string[7::]) if 'b2K7a' in string else slicer(rev_str[0:2] + rev_str[7::])
    result = ''
    for part in code:
        search_part = searcher(part)
        if search_part:
            result = result + search_part
    try:
        return int(result)
    except ValueError:
        raise ValidationError(dict(errors='Invalid ses'))
