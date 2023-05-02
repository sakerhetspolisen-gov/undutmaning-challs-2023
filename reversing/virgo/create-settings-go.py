#!/usr/bin/env python3

"""Expects input from 'xxd -i -c 1000' as key to encrypt flag in argv[1]."""

import sys
import itertools


def main():
    flag = ""
    with open(sys.argv[1]) as flag_file:
        flag = flag_file.read().strip()

    flag_bytes = bytes(flag, "utf-8")

    input_string = sys.stdin.read().strip()

    input_hex = input_string.replace("0x", "").replace(" ", "").split(",")
    input_bytes = [int(h, 16) for h in input_hex]

    # print(flag)
    # print(flag_bytes)
    # print(input_hex)
    # print(input_bytes)

    encrypted = bytes(map(lambda x, y: x^y, flag_bytes, itertools.cycle(input_bytes)))
    encrypted = ",".join([str(int(e)) for e in encrypted])

    # print(encrypted)

    settings_go = f"""
package main

var encrypted = []byte{{{encrypted}}}
"""

    with open("settings.go", "w") as settings_go_file:
        settings_go_file.write(settings_go)


if __name__ == "__main__":
    main()
