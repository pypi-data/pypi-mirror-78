#!/usr/bin/env python


def equal_filter(_str, line_counter, start_from):

    if ' = ' in _str and "$object->" in _str:

        if _str.find(' = ') > _str.find("$object->"):

            if line_counter > start_from:
                return True

    return False


def search_lines(file_path, f_filter, start_from=0):

    with open(file_path) as fp:

        line = fp.readline()
        line_counter = 1
        hit_counter = 0

        while line:

            if f_filter(line, line_counter, start_from):
                print(f"Line {line_counter}: {line}")
                hit_counter += 1

            line = fp.readline()
            line_counter += 1

        print(f"\nfound {hit_counter}  lines with filter {f_filter}")


if __name__ == "__main__":

    _file_path = 'DockingBot'

    search_lines(_file_path, equal_filter, 1602)


