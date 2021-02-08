"""3rd day of advent of code 2020."""


import functools
import operator
import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


TREE = "#"


class MovementVector(typing.NamedTuple):
    delta_rows: int
    delta_columns: int


def solve(movement_vector: MovementVector) -> int:
    collisions = 0
    column = 0
    with open(HERE / INPUT_FILE_NAME) as f:
        path = next(f).strip()
        path_length = len(path)
        while True:
            for _ in range(movement_vector.delta_rows):
                try:
                    path = next(f)
                except StopIteration:
                    return collisions
            else:
                path = path.strip()
                column = (column + movement_vector.delta_columns) % path_length
                if path[column] == TREE:
                    collisions += 1


def main():
    movement_vectors_1 = (MovementVector(delta_rows=1, delta_columns=3),)
    movement_vectors_2 = (
        MovementVector(delta_rows=1, delta_columns=1),
        MovementVector(delta_rows=1, delta_columns=3),
        MovementVector(delta_rows=1, delta_columns=5),
        MovementVector(delta_rows=1, delta_columns=7),
        MovementVector(delta_rows=2, delta_columns=1))
    for movement_vectors in (movement_vectors_1, movement_vectors_2):
        result_set = (
            solve(movement_vector)
            for movement_vector in movement_vectors)
        print(functools.reduce(operator.mul, result_set))


if __name__ == "__main__":
    main()
