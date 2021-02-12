"""14th day of advent of code 2020."""


import itertools
import pathlib
import re
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


MASK_EXTRACTOR = re.compile(r"^mask = ([01X]+)$").search
MEMORY_EXTRACTOR = re.compile(r"^mem\[(\d+)] = (\d+)$").search


def get_values() -> typing.Generator[tuple[int, int], None, None]:
    mask_set = 0
    mask_del = 2 ** 36 - 1
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            if line.startswith("mask"):
                mask_set = 0
                mask_del = 2 ** 36 - 1
                raw_mask = MASK_EXTRACTOR(line.strip()).group(0)
                for index, bit in enumerate(reversed(raw_mask)):
                    if bit == "0":
                        mask_del &= ~(1 << index)
                    elif bit == "1":
                        mask_set |= 1 << index
            else:
                address, value = MEMORY_EXTRACTOR(line.strip()).groups()
                yield int(address), int(value) & mask_del | mask_set


def get_addresses() -> typing.Generator[tuple[int, int], None, None]:
    mask_set = 0
    mask_del = 2 ** 36 - 1
    floating_bits: list[int] = []
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            if line.startswith("mask"):
                mask_set = 0
                mask_del = 2 ** 36 - 1
                floating_bits: list[int] = []
                raw_mask = MASK_EXTRACTOR(line.strip()).group(0)
                for index, bit in enumerate(reversed(raw_mask)):
                    if bit == "X":
                        mask_del &= ~(1 << index)
                        floating_bits.append(index)
                    elif bit == "1":
                        mask_set |= 1 << index
            elif line.startswith("mem"):
                raw_address, value = MEMORY_EXTRACTOR(line.strip()).groups()
                base_address = int(raw_address) & mask_del | mask_set
                value = int(value)
                for bit_set in itertools.product((0, 1),
                                                 repeat=len(floating_bits)):
                    address = base_address
                    for bit, shifts in zip(bit_set, floating_bits):
                        address |= bit << shifts
                    yield address, value
            else:
                raise RuntimeError("Should not get here")


def solve1() -> int:
    return sum({address: value for address, value in get_values()}.values())


def solve2() -> int:
    return sum({address: value for address, value in get_addresses()}.values())


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
