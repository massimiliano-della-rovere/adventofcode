"""4th day of advent of code 2020."""


import pathlib
import re
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


LENGTH_SPLITTER = re.compile(r"^(\d+)(in|cm)$").search


Tester = typing.Callable[[str], bool]
Passport = typing.Dict[str, str]
Regulations = typing.Dict[str, Tester]
Engine = typing.Callable[[Passport, Regulations], bool]


def byr_validator(value: str) -> bool:
    return len(value) == 4 and 1920 <= int(value) <= 2002


def ecl_validator(value: str) -> bool:
    return value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def eyr_validator(value: str) -> bool:
    return len(value) == 4 and 2020 <= int(value) <= 2030


def hgt_validator(value: str) -> bool:
    try:
        length, measure_unit = LENGTH_SPLITTER(value).groups()
    except AttributeError:
        return False

    try:
        length = int(length)
    except ValueError:
        return False

    try:
        a, b = {
            "cm": (150, 193),
            "in": (59, 76)
        }[measure_unit]
    except KeyError:
        return False

    return a <= length <= b


def iyr_validator(value: str) -> bool:
    return len(value) == 4 and 2010 <= int(value) <= 2020


REGULATIONS = {
    "byr": byr_validator,
    "iyr": iyr_validator,
    "eyr": eyr_validator,
    "hgt": hgt_validator,
    "hcl": re.compile(r"^#[0-9a-f]{6}$").search,
    "ecl": ecl_validator,
    "pid": re.compile(r"^\d{9}$").search
}


def key_tester(current_passport: Passport,
               required_keys: Regulations) -> bool:
    return set(required_keys) <= set(current_passport)


def value_tester(current_passport: Passport,
                 required_keys: Regulations) -> bool:
    for key, tester in required_keys.items():
        try:
            value = current_passport[key]
        except KeyError:
            # print(f"missing {key} in {current_passport}")
            return False
        else:
            if not tester(value):
                # print(
                #     f"failed {tester.__name__}/{key}={value}"
                #     f" in {current_passport}")
                return False
    else:
        return True


def solve(test_method: Engine) -> int:
    valid_passports = 0
    current_passport = {}
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            line = line.strip()
            if line:
                # noinspection PyTypeChecker
                current_passport |= dict(
                    pair.split(":")
                    for pair in line.split(" "))
            else:
                if test_method(current_passport, REGULATIONS):
                    valid_passports += 1
                current_passport.clear()
        if test_method(current_passport, REGULATIONS):
            valid_passports += 1
        return valid_passports


def main():
    for test_method in (key_tester, value_tester):
        print(solve(test_method=test_method))


if __name__ == "__main__":
    main()
