#!/usr/bin/env python3

"""Main."""

from os import path
import sys
from cpu import CPU


def main(program_file):
    # if program_file is None:
    #     program_file = "ls8/examples/print8.ls8"
    with open(program_file) as f:
        # program =
        # 1    parse a binary string; convert and return as integer.
        # 2     from a filtered list (strings must be at least 1 character in length)
        # 3       mapped through a function that cleans out any comments, newline strings and spaces
        # 4         read-in from program_file
        program = list(map(lambda n: int(n, 2), list(filter(lambda s: len(s) > 0, list(
            map(lambda code: code.split('#')[0].strip(), f.readlines()))))))
    cpu = CPU()
    cpu.load(program)
    cpu.run()


def resolve_program():
    examples_dir = path.abspath(path.join(path.dirname(__file__), "examples"))
    program = sys.argv[1]
    # program = "stack"  # for debugging
    fname = f"{program.split('/')[-1].split('.')[0]}.ls8"
    program_file = path.join(examples_dir, fname)
    return program_file


if __name__ == "__main__":
    try:
        program_file = resolve_program()
        assert path.exists(program_file)
        main(program_file)
    except AssertionError:
        print(f"cannot find program: {sys.argv[1]}")
    except IndexError as ie:
        print("\n    ---------------------- ")
        print("      REQUIRES A PROGRAM ")
        print("    ---------------------- \n")
        print("***   USAGE: python3 ls8.py PROGRAM   ***")
        print('\n*** EXAMPLE: python3 ls8.py mult ***\n')
