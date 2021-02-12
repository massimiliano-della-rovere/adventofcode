"""13th day of advent of code 2020."""


import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


Now = int
BusIDs = typing.Sequence[int]


def get_now_and_bus_ids() -> tuple[Now, BusIDs]:
    with open(HERE / INPUT_FILE_NAME) as f:
        return (
            int(f.readline().strip()),
            sorted(
                int(number)
                for number in f.readline().strip().split(",")
                if number.isdigit()))


def solve1() -> int:
    now, bus_ids = get_now_and_bus_ids()
    ret_bus = None
    waiting_time = float("+inf")
    for bus_id in bus_ids:
        missed_by = now % bus_id
        if missed_by:
            delta = bus_id - missed_by
            if delta < waiting_time:
                ret_bus = bus_id
                waiting_time = delta
        else:
            return 0
    return ret_bus * waiting_time


def get_data() -> typing.Sequence[tuple[int, int]]:
    with open(HERE / INPUT_FILE_NAME) as f:
        f.readline()
        return tuple(
            (int(string), index)
            for index, string in enumerate(f.readline().strip().split(","))
            if string.isdigit())


def solve2() -> int:
    (product_of_factors, _), *data = get_data()
    t = 0
    for bus_id, offset in data:
        while (t + offset) % bus_id:
            t += product_of_factors
        product_of_factors *= bus_id
    return t


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
