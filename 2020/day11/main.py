"""11th day of advent of code 2020."""


import enum
import itertools
import operator
import pathlib
import typing


HERE = pathlib.Path(__file__).parent
INPUT_FILE_NAME = "input.txt"


class SpotStatus(enum.Enum):
    EMPTY = "L"
    OCCUPIED = "#"
    FLOOR = "."


class MovementVector(typing.NamedTuple):
    row_direction: int
    column_direction: int


MOVEMENT_VECTORS = tuple(
    MovementVector(row_direction, column_direction)
    for row_direction in range(-1, 2)
    for column_direction in range(-1, 2)
    if row_direction or column_direction)


SpotNumber = int
RawSeatMap = typing.Sequence[str]
Seats = typing.Sequence[SpotStatus]
Processor = typing.Callable[[SpotNumber], SpotStatus]


def get_2d_seat_map() -> RawSeatMap:
    with open(HERE / INPUT_FILE_NAME) as f:
        return tuple(line.strip() for line in f)


class SeatMap:
    def __init__(self,
                 _2d_map_model: RawSeatMap,
                 use_high_tolerance: bool,
                 use_adjacent_spotting: bool):
        self._use_high_tolerance = use_high_tolerance
        self._tolerance = 5 if use_high_tolerance else 4
        self._use_adjacent_spotting = use_adjacent_spotting
        self._get_hot_spots: typing.Callable[[int], Seats] = (
            self.the_8_adjancent_spots
            if use_adjacent_spotting
            else self.long_range_scan_for_spots)
        self._map_2d = _2d_map_model
        self._map_height = len(_2d_map_model)
        self._map_width = len(_2d_map_model[0])
        self._map_1d: Seats = tuple(
            map(SpotStatus, itertools.chain.from_iterable(_2d_map_model)))
        if (chars := set(self._map_1d)) > set(SpotStatus):
            raise ValueError(f"invalid map {chars=}")
        self._map_length = len(self._map_1d)
        self._work_map: typing.Union[Seats, None] = None
        self._status_mapper: typing.TypedDict[SpotStatus, Processor] = {
            status: getattr(self, f"_process_{status.name.lower()}_spot")
            for status in SpotStatus
        }
        print(f"w={self._map_width} x h={self._map_height}"
              f" = {self._map_width * self._map_height}")

    def __str__(self) -> str:
        if self._work_map:
            # noinspection PyTypeChecker
            return "\n".join(
                "".join(map(operator.attrgetter("value"), spots))
                for r in range(self._map_height)
                for spots in self._work_map[
                         r * self._map_width:(r + 1) * self._map_width])
        else:
            return "\n".join(self._map_2d)

    def the_8_adjancent_spots(self, spot_number: SpotNumber) -> Seats:
        map_model: Seats = self._work_map or self._map_1d
        spot_row, spot_column = divmod(spot_number, self._map_width)
        return tuple(
            map_model[self._map_width * r + c + spot_number]
            for r in range(-1 if spot_row > 0 else 0,
                           2 if spot_row < self._map_height - 1 else 1)
            for c in range(-1 if spot_column > 0 else 0,
                           2 if spot_column < self._map_width - 1 else 1)
            if r or c)

    def long_range_scan_for_spots(self, spot_number: SpotNumber) -> Seats:
        map_model: Seats = self._work_map or self._map_1d
        spot_row, spot_column = divmod(spot_number, self._map_width)
        ret = []
        for movement_vector in MOVEMENT_VECTORS:
            row, column = spot_row, spot_column
            while True:
                row += movement_vector.row_direction
                column += movement_vector.column_direction
                if (
                        row < 0 or row >= self._map_height
                        or
                        column < 0 or column >= self._map_width
                ):
                    break
                else:
                    spot_status = map_model[self._map_width * row + column]
                    if spot_status != SpotStatus.FLOOR:
                        ret.append(spot_status)
                        break
        return tuple(ret)

    def _process_empty_spot(self, spot_number: SpotNumber) -> SpotStatus:
        adjacent_spots = self._get_hot_spots(spot_number)
        return (
            SpotStatus.OCCUPIED
            if all(spot != SpotStatus.OCCUPIED for spot in adjacent_spots)
            else SpotStatus.EMPTY)

    @staticmethod
    def _process_floor_spot(spot_number: SpotNumber) -> SpotStatus:
        return SpotStatus.FLOOR

    def _process_occupied_spot(self, spot_number: int) -> SpotStatus:
        adjacent_spots = self._get_hot_spots(spot_number)
        return (
            SpotStatus.EMPTY
            if self._tolerance <= sum(1
                                      for spot in adjacent_spots
                                      if spot == SpotStatus.OCCUPIED)
            else SpotStatus.OCCUPIED)

    def evolve(self) -> int:
        self._work_map = self._map_1d
        current_status = hash(self._work_map)
        for iteration in itertools.count(1):
            self._work_map = tuple(
                self._status_mapper[spot_status](spot_number)
                for spot_number, spot_status in enumerate(self._work_map))

            new_status = hash(self._work_map)
            # print(f"{iteration=}, status: {current_status} => {new_status}")
            if new_status == current_status:
                try:
                    return sum(
                        1
                        for spot in self._work_map
                        if spot == SpotStatus.OCCUPIED)
                finally:
                    self._work_map = None
            else:
                current_status = new_status


def solve1() -> int:
    return SeatMap(
        _2d_map_model=get_2d_seat_map(),
        use_high_tolerance=False,
        use_adjacent_spotting=True
    ).evolve()


def solve2() -> int:
    return SeatMap(
        _2d_map_model=get_2d_seat_map(),
        use_high_tolerance=True,
        use_adjacent_spotting=False
    ).evolve()


def main():
    print(solve1())
    print(solve2())


if __name__ == "__main__":
    main()
