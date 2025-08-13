import copy
from random import random, randrange, choice
from typing import Callable, Generator, List, Optional, Tuple


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height

        self._data: List[List[int]] = [[0 for j in range(height)] for i in range(width)]

    def __repr__(self) -> str:
        rep = f"({self.height}x{self.width}), score={self.score()}\n"
        for row in self:
            rep += "|"
            for cell in row:
                rep += f" {cell if cell != 0 else ' '}\t|"
            rep += "\n"
        return rep

    def __getitem__(self, coords: Tuple[int, int]) -> int:
        return self._data[coords[1]][coords[0]]

    def __setitem__(self, coords: Tuple[int, int], value: int) -> None:
        self._data[coords[1]][coords[0]] = value

    def __iter__(self) -> Generator:
        for row in self._data:
            yield row

    def __len__(self) -> int:
        return self.width * self.height

    def reset(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self._data[x][y] = 0

    def _iterate(
        self,
        func: Callable[[int, int], Optional[int]],
        *,
        filter: Optional[Callable[[int, int], bool]],
    ) -> List[int]:
        results = []
        for x in range(self.width):
            for y in range(self.height):
                if not filter or not filter(x, y):
                    continue

                res = func(x, y)
                if res is not None:
                    results.append(res)
        return results

    def _shift(self, x: int, y: int, x_direction: int, y_direction: int) -> None:
        if self._data[y][x] == 0:
            return

        new_y = y
        # > 0 up, < 0 down, 0 nothing
        while (
            new_y - y_direction != y
            and new_y - y_direction >= 0
            and new_y - y_direction < self.height
            and (
                self._data[new_y - y_direction][x] == 0
                or self._data[new_y - y_direction][x] == self._data[y][x]
            )
        ):
            new_y -= y_direction

        new_x = x
        while (
            new_x - x_direction != x
            and new_x - x_direction >= 0
            and new_x - x_direction < self.height
            and (
                self._data[y][new_x - x_direction] == 0
                or self._data[y][new_x - x_direction] == self._data[y][x]
            )
        ):
            new_x -= x_direction

        # print(f"{(x, y)} -> {(x, new_y)}")
        if new_y != y or new_x != x:
            if self._data[new_y][new_x] == self._data[y][x]:
                self._data[new_y][new_x] = self._data[y][x] * 2
            else:
                self._data[new_y][new_x] = self._data[y][x]
            self._data[y][x] = 0

    def shift_up(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self._shift(x, y, 0, 1)

    def shift_down(self) -> None:
        for x in reversed(range(self.width)):
            for y in reversed(range(self.height)):
                self._shift(x, y, 0, -1)

    def shift_left(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self._shift(x, y, 1, 0)

    def shift_right(self) -> None:
        for y in reversed(range(self.height)):
            for x in reversed(range(self.width)):
                self._shift(x, y, -1, 0)

    def step(self, move: str) -> bool:
        before = copy.deepcopy(self._data)

        match move:
            case "up" | "w":
                self.shift_up()
            case "down" | "s":
                self.shift_down()
            case "right" | "d":
                self.shift_right()
            case "left" | "a":
                self.shift_left()

        if self._data == before and self.full():
            return False

        self._generate_random()
        return True

    def render(self) -> None:
        print(self)

    def full(self) -> bool:
        for row in self:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def done(self) -> bool:
        return self.full()

    def _generate_random(self) -> None:
        if self.full():
            return

        empty_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self._data[y][x] == 0
        ]
        x, y = choice(empty_cells)

        self._data[y][x] = 4 if random() < 0.1 else 2  # 10% 4, 90% 2

    def score(self) -> float:
        score = float("-inf")
        for row in self:
            for cell in row:
                score = max(score, cell)
        return score

    def tick(self) -> None:
        pass


"""

[0][0][1]
[0][1][0]
[0][0][1]

[1, 1] |> [1, 0] == 0                   => [1, 0]
[2, 2] |> [2, 1] == 0 |> [2, 0] != 0    => [2, 1]
[2, 0]                                  => [2, 0]

[1, 0]                                  => [1, 0]
[2, 0]                                  => [2, 0]
[2, 1] |> [2, 0] != 0 + [2, 1]          => [2, 1]

"""
