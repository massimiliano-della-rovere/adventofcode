"""14th day of advent of code 2020."""


import itertools
import pathlib
import re
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


MASK_EXTRACTOR = re.compile(r"^mask = ([01X]+)$").search
MEMORY_EXTRACTOR = re.compile(r"^mem\[(\d+)] = (\d+)$").search


class Mask:
    def __init__(self, mask: str):
        self._mask_len = len(mask)
        self._mask_set = 0
        self._mask_del = 2 ** self._mask_len - 1
        self._set(mask)

    def _set(self, mask: str) -> None:
        for index, bit in enumerate(reversed(mask)):
            if bit == "0":
                self._mask_del &= ~(1 << index)
            elif bit == "1":
                self._mask_set |= 1 << index
            elif bit != "X":
                raise ValueError(bit)

    def __call__(self, value: int) -> int:
        return value & self._mask_del | self._mask_set


def get_values() -> typing.Generator[tuple[int, int], None, None]:
    mask = None
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            if line.startswith("mask"):
                mask = Mask(MASK_EXTRACTOR(line.strip()).group(1))
            else:
                address, value = MEMORY_EXTRACTOR(line.strip()).groups()
                yield int(address), mask(int(value))


class FloatingMask(Mask):
    def __init__(self, mask: str):
        self._floating_bits: list[int] = []
        super().__init__(mask)

    def _set(self, mask: str) -> None:
        for index, bit in enumerate(reversed(mask)):
            if bit == "X":
                self._mask_del &= ~(1 << index)
                self._floating_bits.append(index)
            elif bit == "1":
                self._mask_set |= 1 << index
            elif bit != "0":
                raise ValueError(bit)

    def __call__(self, value: int) -> typing.Sequence[int]:
        value = value & self._mask_del | self._mask_set
        for bit_set in itertools.product((0, 1),
                                         repeat=len(self._floating_bits)):
            copy = value
            for bit, shifts in zip(bit_set, self._floating_bits):
                copy |= bit << shifts
            yield copy


def get_addresses() -> typing.Generator[tuple[int, int], None, None]:
    mask = None
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            if line.startswith("mask"):
                mask = FloatingMask(MASK_EXTRACTOR(line.strip()).group(1))
            elif line.startswith("mem"):
                raw_address, value = MEMORY_EXTRACTOR(line.strip()).groups()
                for address in mask(int(raw_address)):
                    yield address, int(value)
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
