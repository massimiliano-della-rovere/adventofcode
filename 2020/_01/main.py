"""1st day of advent of code 2020."""


import functools
import itertools
import operator
import pathlib


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


TOTAL = 2020


def solve(group_size: int, total: int) -> int:
    with open(HERE / INPUT_FILE_NAME) as f:
        for group in itertools.combinations(map(int, f), group_size):
            if sum(group) == total:
                return functools.reduce(operator.mul, group)
        else:
            raise RuntimeError("Should not get here")


def main():
    runner = functools.partial(solve, total=TOTAL)
    for group_size in (2, 3):
        print(runner(group_size=group_size))


if __name__ == "__main__":
    main()
