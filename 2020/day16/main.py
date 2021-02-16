"""16th day of advent of code 2020."""


import collections
import functools
import itertools
import operator
import pathlib
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
    name, intervals = line.split(": ")
    return Rule(
        name,
        tuple(
            tuple(int(value) for value in interval.split("-"))
            for interval in intervals.split(" or ")))


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
    ret["my ticket"] = ret["my ticket"][0]
    return {k: tuple(v) for k, v in ret.items()}


def solve1() -> tuple[int, dict[str, typing.Union[Rules, Ticket]]]:
    data = get_values()
    rules = data["rules"]
    invalid_values = []
    valid_tickets = []
    invalid_tickets = []
    for ticket in data["nearby tickets"]:
        for value in ticket:
            if not any(
                    min_value <= value <= max_value
                    for rule in rules
                    for min_value, max_value in rule.ranges):
                invalid_values.append(value)
                invalid_tickets.append(ticket)
                break
        else:
            valid_tickets.append(ticket)
    data["valid tickets"] = tuple(valid_tickets)
    data["invalid tickets"] = tuple(invalid_tickets)
    return sum(invalid_values), data


def solve2(data: dict[str, typing.Union[Rules, Ticket]]) -> int:
    rules = data["rules"]
    possible_matches = collections.defaultdict(set)
    tickets = tuple(
        itertools.chain(data["valid tickets"], (data["my ticket"],)))
    for part_index in range(len(data["my ticket"])):
        for rule_id, rule in enumerate(rules):
            if all(
                    any(min_value <= ticket[part_index] <= max_value
                        for min_value, max_value in rule.ranges)
                    for ticket in tickets
            ):
                possible_matches[part_index].add(rule_id)

    guessed = {}
    while possible_matches:
        removed = {
            possible_matches.pop(part_id).pop(): part_id
            for part_id, rule_ids in list(possible_matches.items())
            if len(rule_ids) == 1}
        guessed.update(removed)
        for rule_id in removed:
            for part_ids in possible_matches.values():
                part_ids.remove(rule_id)

    return functools.reduce(
        operator.mul,
        (
            data["my ticket"][guessed[rule_index]]
            for rule_index, rule in enumerate(rules)
            if rule.name.startswith("departure")
        ))


def main():
    result, data = solve1()
    print(result)
    print(solve2(data))


if __name__ == "__main__":
    main()
