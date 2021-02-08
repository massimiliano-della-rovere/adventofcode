"""6th day of advent of code 2020."""


import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


def solve1() -> int:
    total = 0
    current_group = set()
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            line = line.strip()
            if line:
                current_group |= set(line)
            else:
                total += len(current_group)
                current_group.clear()
        total += len(current_group)
    return total


def solve2() -> int:
    total = 0
    current_group = set()
    operation = current_group.update
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            line = line.strip()
            if line:
                operation(set(line))
                operation = current_group.intersection_update
            else:
                total += len(current_group)
                current_group.clear()
                operation = current_group.update
        total += len(current_group)
    return total


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
