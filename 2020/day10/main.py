"""10th day of advent of code 2020."""


import collections
import itertools
import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


JOLT_LIMIT = 3


Adapters = typing.Sequence[int]


def list_adapters() -> Adapters:
    with open(HERE / INPUT_FILE_NAME) as f:
        return tuple(sorted(int(line) for line in f))


def solve1() -> int:
    deltas = collections.Counter()
    current_jolts = 0
    for adapter in list_adapters():
        delta = adapter - current_jolts
        if delta > JOLT_LIMIT:
            raise RuntimeError("Should not get here")
        deltas[delta] += 1
        current_jolts = adapter
    deltas[3] += 1  # we are still 3 Jolts below the device
    return deltas[1] * deltas[3]


def solve2() -> int:
    valid_combos = collections.defaultdict(int, {0: 1})
    adapters = list_adapters()
    for adapter in itertools.chain(adapters, (adapters[-1] + JOLT_LIMIT,)):
        new_valid_combos = collections.defaultdict(int)

        jolts = adapter - JOLT_LIMIT
        if jolts >= 0 and jolts in valid_combos:
            new_valid_combos[adapter] = valid_combos[jolts]

        for jolts in range(adapter - 1, adapter - JOLT_LIMIT, -1):
            if jolts >= 0 and jolts in valid_combos:
                quantity = valid_combos[jolts]
                new_valid_combos[adapter] += quantity
                new_valid_combos[jolts] = quantity

        valid_combos = new_valid_combos

    if len(valid_combos) != 1:
        raise RuntimeError("Should not get here")
    else:
        return next(iter(valid_combos.values()))


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
