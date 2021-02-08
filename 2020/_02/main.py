"""2nd day of advent of code 2020."""


import pathlib
import re
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


REGEXP = r"^(?P<a>\d+)-(?P<b>\d+) (?P<letter>\w): (?P<password>.*)$"
PARSER = re.compile(REGEXP).search


def test_1(data):
    min_occurrencies = int(data["a"])
    max_occurrencies = int(data["b"])
    occurrencies = data["password"].count(data["letter"])
    return min_occurrencies <= occurrencies <= max_occurrencies


def test_2(data):
    position_1 = int(data["a"]) - 1
    position_2 = int(data["b"]) - 1
    password = data["password"]
    letter_1 = password[position_1]
    letter_2 = password[position_2]
    letter = data["letter"]
    return (letter_1 == letter) ^ (letter_2 == letter)


def solve(tester: typing.Callable[[dict], bool]) -> int:
    count = 0
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            if tester(PARSER(line.strip()).groupdict()):
                count += 1
        return count


def main():
    for tester in (test_1, test_2):
        print(solve(tester=tester))


if __name__ == "__main__":
    main()
