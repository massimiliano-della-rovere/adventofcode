"""9th day of advent of code 2020."""


import itertools
import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


WINDOW_SIZE = 25


DataDump = typing.Sequence[int]


def dump_xmas_values() -> DataDump:
    with open(HERE / INPUT_FILE_NAME) as f:
        return tuple(int(line) for line in f)


def solve1() -> int:
    values = dump_xmas_values()
    for i in range(WINDOW_SIZE, len(values)):
        number = values[i]
        for a, b in itertools.combinations(values[i - WINDOW_SIZE:i], 2):
            if a + b == number:
                break
        else:
            return number
    else:
        raise RuntimeError("Should not get here")


def solve2_less_cpu() -> int:
    values = dump_xmas_values()
    weakness = solve1()
    for window_start in range(0, len(values)):
        for window_size in range(2, len(values)):
            window = values[window_start:window_start + window_size]
            total = sum(window)
            if total < weakness:
                continue
            if total == weakness:
                return min(window) + max(window)
            if total > weakness:
                break
    else:
        raise RuntimeError("Should not get here")


def solve2_less_ram() -> int:
    values = dump_xmas_values()
    weakness = solve1()
    for window_start in range(0, len(values)):
        total = 0
        min_value = float("+inf")
        max_value = float("-inf")
        for number in itertools.islice(values, window_start, None):
            total += number
            min_value = min(min_value, number)
            max_value = max(max_value, number)
            if total < weakness:
                continue
            if total == weakness:
                return min_value + max_value
            if total > weakness:
                break
    else:
        raise RuntimeError("Should not get here")


def main():
    print(solve1())
    print(solve2_less_ram())
    print(solve2_less_cpu())


if __name__ == "__main__":
    main()
