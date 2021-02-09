"""5th day of advent of code 2020."""


import bisect
import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


Processor = typing.Callable[[typing.Iterable], int]


def find_my_seat(values: typing.Iterable) -> int:
    all_seat_ids = list(range(0, 127 * 8 + 7 + 1))
    for value in values:
        all_seat_ids.remove(value)

    middle_seat_id = 511
    left_index = bisect.bisect_left(all_seat_ids, middle_seat_id)
    right_index = bisect.bisect_right(all_seat_ids, middle_seat_id)
    left_delta = middle_seat_id - left_index
    right_delta = right_index - middle_seat_id
    return (
        all_seat_ids[left_index]
        if left_delta < right_delta
        else all_seat_ids[right_index])


def translate_seat_code(seat_code: str) -> int:
    row_base2 = seat_code[:7].replace("F", "0").replace("B", "1")
    seat_row = int(row_base2, base=2)

    column_base2 = seat_code[7:].replace("L", "0").replace("R", "1")
    seat_column = int(column_base2, 2)

    seat_id = seat_row * 8 + seat_column
    return seat_id


def solve(processor: Processor):
    with open(HERE / INPUT_FILE_NAME) as f:
        return processor(
            translate_seat_code(line.strip())
            for line in f)


def main():
    for processor in (max, find_my_seat):
        print(solve(processor))


if __name__ == "__main__":
    main()
