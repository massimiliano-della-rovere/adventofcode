"""7th day of advent of code 2020."""


import collections
import functools
import operator
import pathlib
import re
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


CONTAINED_BAGS_PARSER = re \
    .compile(r"^(?P<quantity>\d) (?P<bag>\w+ \w+) bags?$") \
    .search


class Regulation(typing.NamedTuple):
    quantity: int
    bag: str


Bag = str
Regulations = typing.Dict[Bag, typing.Sequence[Regulation]]
BagHierarchy = typing.Dict[Bag, typing.FrozenSet[Bag]]
BagCount = typing.Dict[Bag, typing.Dict[Bag, int]]


def create_regulations_tree() -> Regulations:
    regulations = {}
    with open(HERE / INPUT_FILE_NAME) as f:
        for line in f:
            container, rest = line.strip().rstrip(".").split(" bags contain ")
            if rest == "no other bags":
                regulations[container] = ()
            else:
                contained = []
                for parts in rest.split(", "):
                    data = CONTAINED_BAGS_PARSER(parts).groupdict()
                    data["quantity"] = int(data["quantity"])
                    contained.append(Regulation(**data))
                regulations[container] = tuple(contained)
    return regulations


def calculate_containers(regulation_set: Regulations) -> BagHierarchy:
    """
    Given a specific bag (the key of the returned dict),
    which bags (the value of the returned key) do contain it?
    """
    ret = collections.defaultdict(set)
    stack = []
    containers = []
    for bag, _regulations in regulation_set.items():
        containers.append(bag)
        regulations = iter(_regulations)
        while True:
            try:
                regulation = next(regulations)
            except StopIteration:
                containers.pop()
                try:
                    regulations = stack.pop()
                except IndexError:
                    break
            else:
                contained = regulation.bag

                ret[contained] |= set(containers)
                containers.append(contained)

                stack.append(regulations)
                regulations = iter(regulation_set[contained])
    return {bag: frozenset(containers) for bag, containers in ret.items()}


def calculate_contained_bags(regulation_set: Regulations) -> BagCount:
    """
    Given a specific bag (the key of the returned dict),
    how many bags per type (the value of the returned dict) does it contain?
    """
    ret = collections.defaultdict(collections.Counter)
    stack = []
    multipliers = []
    for bag, _regulations in regulation_set.items():
        multipliers.append(1)
        regulations = iter(_regulations)
        while True:
            try:
                regulation = next(regulations)
            except StopIteration:
                multipliers.pop()
                try:
                    regulations = stack.pop()
                except IndexError:
                    break
            else:
                total_quantity = regulation.quantity * functools.reduce(
                    operator.mul,
                    multipliers)
                ret[bag] += collections.Counter(
                    {regulation.bag: total_quantity})
                multipliers.append(regulation.quantity)

                stack.append(regulations)
                regulations = iter(regulation_set[regulation.bag])
    return {bag: dict(count) for bag, count in ret.items()}


def solve1() -> int:
    regulations = create_regulations_tree()
    contained = calculate_containers(regulations)
    return len(contained["shiny gold"])


def solve2() -> int:
    regulations = create_regulations_tree()
    contained = calculate_contained_bags(regulations)
    return sum(contained["shiny gold"].values())


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
