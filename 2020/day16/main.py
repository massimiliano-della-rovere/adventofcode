"""16th day of advent of code 2020."""


import collections
import itertools
import pathlib
import re
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


Range = typing.Sequence[int]


class Rule(typing.NamedTuple):
    name: str
    ranges: typing.Sequence[Range]


Rules = typing.Sequence[Rule]
Ticket = typing.Sequence[int]
Tickets = typing.Sequence[Ticket]


def import_rule(line: str) -> Rule:
    name, ranges = line.split(": ")[1]
    return Rule(
        name,
        tuple(
            tuple(int(value) for value in interval.split("-"))
            for interval in ranges.split(" or ")))


def import_ticket(line: str) -> Ticket:
    return tuple(int(value) for value in line.split(","))


def get_values() -> dict[str, typing.Union[Rules, Ticket]]:
    ret = collections.defaultdict(list)
    engine = iter((("rules", import_rule),
                   ("my ticket", import_ticket),
                   ("nearby tickets", import_ticket)))
    with open(HERE / INPUT_FILE_NAME) as f:
        key, importer = next(engine)
        for line in f:
            if line := line.strip():
                ret[key].append(importer(line))
            else:
                key, importer = next(engine)
                f.readline()
    return {k: tuple(v) for k, v in ret.items()}


def solve1() -> int:
    data = get_values()
    rules = data["rules"]
    invalid = []
    for ticket in data["nearby tickets"]:
        for value in ticket:
            if not any(
                    min_value <= value <= max_value
                    for rule in rules
                    for min_value, max_value in rule):
                invalid.append(value)
                break
    return sum(invalid)


def get_valid_tickets(rules: Rules,
                      tickets: Tickets) -> typing.Generator[Ticket, None, None]:
    for ticket in tickets:
        if any(
                min_value <= value <= max_value
                for value in ticket
                for rule in rules
                for min_value, max_value in rule):
            yield ticket


# def match(ticket: Ticket, rules: Rules) -> typing.TypedDict[int, list[int]]:




# def solve2() -> int:
#     data = get_values()
#     rules = data["rules"]
#     part_rule_match = {
#         part_index: list(range(len(rules)))
#         for part_index, rule in enumerate(data["my ticket"])
#     }
#     for valid_ticket in get_valid_tickets(rules, data["nearby tickets"]):
#         for part_index, part in enumerate(valid_ticket):
#             if len(part_rule_match[part_index]) > 1:
#                 part_rule_match[part_index] = [
#
#                 ]


def main():
    print(solve1())
    # print(solve2())


if __name__ == "__main__":
    main()
