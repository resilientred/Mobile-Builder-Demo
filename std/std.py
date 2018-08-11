import hashlib
import logging

from std.error import data_error
from std.error.data_error import DataError


# Convert Object to Boolean
def obj_to_bool(obj)-> bool:
    if type(obj) is str:
        return str_to_bool(obj)
    if type(obj) is int:
        return int_to_bool(obj)


# Convert String to Boolean
# "true" -> True
def str_to_bool(text: str) -> bool:
    if text == "true":
        return True
    if text == "false":
        return False
    raise AttributeError


# Convert Integer to Boolean
# 1 -> True
def int_to_bool(num: int) -> bool:
    if num == 0:
        return False
    if num > 0:
        return True
    raise AttributeError


# Convert String to Integer
# "true" -> 1
def str_to_int(text):
    if text == "true":
        return 1
    if text == "false":
        return 0
    raise AttributeError


# Get items path and merge to whole PATH
def merge(path: str, *args) -> str:
    slash = '/'

    if path[-1:] == slash:
        path = path[:-1]
    result = path

    if path and args:
        for arg in args:
            if str(arg)[0] == slash:
                result += str(arg)
            else:
                result += slash + str(arg)

    return result


# Sorting map object order by ASC
def sort_dict(map: dict) -> dict:
    logging.debug(map)
    sorted(map.items(), key=lambda t: t[0])
    return dict(map)


# Create MD5 hash from Text
def hashing(text: str) -> str:
    test_encode = str(text).encode('utf-8')
    return hashlib.md5(test_encode).hexdigest()


def validate_field(filed):
    if filed is None:
        raise DataError(DataError.not_found, DataError.data_invalid_mes % "UNKNOWN")
    return filed
