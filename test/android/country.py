import os

import time

from std.std import merge


def replace_strings(bundle, new_bundle):
    # Begin function work
    count_total = 0
    total_replace = 0
    count_error = 0

    for path, dirs, files in os.walk("/Users/andrew/PycharmProjects/python-build-script/test/android/assets", True):
        for cur_name in files:
            print(files)
            count_total += 1
            file_path = merge(path, cur_name)
            try:
                text = open(file_path).read()
                if bundle in text:
                    open(file_path, 'w').write(text.replace(bundle, new_bundle))
                    total_replace += 1

            except ValueError:
                count_error += 1