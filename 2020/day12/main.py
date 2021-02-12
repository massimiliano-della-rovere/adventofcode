"""12th day of advent of code 2020."""


import abc
import dataclasses
import enum
import math
import operator
import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


real = operator.attrgetter("real")
imag = operator.attrgetter("imag")


CM2D = typing.TypeVar("CM2D", bound="Matrix2D")


@dataclasses.dataclass(init=False, frozen=True)
class ComplexMatrix2D:
    def __init__(self, v1: complex, v2: complex):
        object.__setattr__(self, "_values", (v1, v2))

    @classmethod
    def from_iterable(cls: typing.Type[CM2D],
                      iterable: typing.Iterable[complex]) -> CM2D:
        return cls(*tuple(iterable))

    def __iter__(self):
        return iter(getattr(self, "_values"))

    @typing.overload
    def __mul__(self, other: complex) -> complex:
        pass

    def __mul__(self, other):
        return complex(
            *tuple(
                sum(f(vector) * f(other) for f in (real, imag))
                for vector in self))


class Direction(enum.Enum):
    NORTH = 0 + 1j
    WEST = -1 + 0j
    SOUTH = 0 - 1j
    EAST = +1 + 0j


DIRECTION_MAPPER = {
    "N": Direction.NORTH.value,
    "E": Direction.EAST.value,
    "W": Direction.WEST.value,
    "S": Direction.SOUTH.value
}


ROTATION_MAPPER = {
    direction: {
        math.degrees(theta): ComplexMatrix2D(
            +math.cos(theta) + 1j * sign * math.sin(theta),
            - sign * math.sin(theta) + 1j * math.cos(theta))
        for theta in (math.pi * 0.5, math.pi, math.pi * 1.5)
    }
    for direction, sign in (("L", -1), ("R", +1))
}


class Instruction(typing.NamedTuple):
    what: str
    how_much: int


Instructions = typing.Sequence[Instruction]


def get_instructions() -> typing.Generator[Instruction, None, None]:
    with open(HERE / INPUT_FILE_NAME) as f:
        # for line in ("F10", "N3", "F7", "R90", "F11"):  # result 286 for part2
        for line in f:
            yield Instruction(line[0], int(line[1:].strip()))


class Ship(metaclass=abc.ABCMeta):
    def __init__(self,
                 *,
                 heading_vector: complex,
                 ship_position: complex = 0 + 0j):
        self._initial_ship_position = ship_position
        self._ship_position = ship_position
        self._current_instruction: typing.Union[None, Instruction] = None
        self._initial_heading_vector = heading_vector
        self._heading_vector = heading_vector
        self._action_mapper = {
            "N": self._move,
            "E": self._move,
            "W": self._move,
            "S": self._move,
            "F": self._forward,
            "L": self._rotate,
            "R": self._rotate
        }

    def reset(self):
        self._ship_position = self._initial_ship_position
        self._heading_vector = self._initial_heading_vector

    def manhattan_distance(self):
        return int(
            abs(self._ship_position.real) + abs(self._ship_position.imag))

    def _move(self) -> complex:
        vector = DIRECTION_MAPPER[self._current_instruction.what]
        return vector * self._current_instruction.how_much

    def _forward(self) -> complex:
        return self._heading_vector * self._current_instruction.how_much

    def _rotate(self) -> complex:
        degrees = float(self._current_instruction.how_much)
        matrix = ROTATION_MAPPER[self._current_instruction.what][degrees]
        return matrix * self._heading_vector

    def run(self, instructions: typing.Iterator[Instruction]):
        print(f"{self._ship_position=} {self._heading_vector=}")
        for self._current_instruction in instructions:
            try:
                action = self._action_mapper[self._current_instruction.what]
            except KeyError:
                raise RuntimeError("Should not get here")
            else:
                action()
            print(f"\n{self._current_instruction=}")
            print(f"{self._ship_position=} {self._heading_vector=}")


class SimpleShip(Ship):
    def _move(self) -> None:
        self._ship_position += super()._move()

    def _forward(self) -> None:
        self._ship_position += super()._forward()

    def _rotate(self) -> None:
        self._heading_vector = super()._rotate()


class WaypointShip(Ship):
    def _move(self) -> None:
        self._heading_vector += super()._move()

    def _forward(self) -> None:
        self._ship_position += super()._forward()

    def _rotate(self) -> None:
        self._heading_vector = super()._rotate()


def main():
    for ship_class, heading in (
            (SimpleShip, Direction.EAST.value),
            (
                    WaypointShip,
                    10 * Direction.EAST.value + 1 * Direction.NORTH.value
            )
    ):
        ship = ship_class(heading_vector=heading)
        ship.run(get_instructions())
        print(ship.manhattan_distance())


if __name__ == "__main__":
    main()
