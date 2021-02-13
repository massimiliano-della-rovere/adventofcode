"""15th day of advent of code 2020."""


import collections
import itertools
import pathlib
import re
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


MASK_EXTRACTOR = re.compile(r"^mask = ([01X]+)$").search
MEMORY_EXTRACTOR = re.compile(r"^mem\[(\d+)] = (\d+)$").search


def get_values() -> typing.Sequence[int]:
    with open(HERE / INPUT_FILE_NAME) as f:
        return tuple(map(int, f.readline().strip().split(",")))


class Tail2:
    def __new__(cls, iterator=()):
        return collections.deque(iterator, maxlen=2)


def calculate_next(last_turn: int) -> int:
    numbers = get_values()
    log = {}
    for turn_last_seen, number in enumerate(numbers, 1):
        log.setdefault(number, Tail2()).append(turn_last_seen)
    last_number = numbers[-1]

    for turn in itertools.count(1 + len(numbers)):
        tail2 = log[last_number]
        if len(tail2) == 1:
            last_number = 0
        else:
            last_number = tail2[1] - tail2[0]
        log.setdefault(last_number, Tail2()).append(turn)

        if turn == last_turn:
            return last_number


def solve1() -> int:
    return calculate_next(2020)


def solve2() -> int:
    return calculate_next(30000000)


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
