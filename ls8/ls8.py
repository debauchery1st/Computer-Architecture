#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU


def main(program_file):
    if program_file is None:
        program_file = "ls8/examples/print8.ls8"
    with open(program_file) as f:
        program = list(map(lambda n: int(n, 2), list(filter(lambda s: len(s) > 0, list(
            map(lambda code: code.split('#')[0].strip(), f.readlines()))))))
    cpu = CPU()
    cpu.load(program)
    cpu.run()


if __name__ == "__main__":
    try:
        source = sys.argv[0]
        program = sys.argv[1]
    except IndexError as ie:
        print("\n    ---------------------- ")
        print("      REQUIRES A PROGRAM ")
        print("    ---------------------- \n")
        print("***   USAGE: python3 ls8.py PROGRAM   ***")
        print('\n*** EXAMPLE: python3 ls8.py examples/print8.ls8 ***\n')
        exit(0)
    main(program)
