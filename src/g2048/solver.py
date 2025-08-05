from time import sleep
from typing import Any, Callable, Tuple

from ..utils.cli import cls
from .board import Board


class Solver:
    def __init__(self, method_name: str, method: Callable[[Any, Board], str]) -> None:
        self.method_name = method_name
        self.method = method
        self.turns = 0

    def solve(
        self,
        board: Board,
        iteration: int,
        prev_score: Tuple[float, int, str] = (0, 0, ""),
        max_score: Tuple[float, int, str] = (0, 0, ""),
    ) -> None:
        while True:
            cls()
            print(
                f"current_iteration={iteration}, turn={self.turns}, current_score={(self.method_name, board.score())}, max_score={max_score}, prev_score={prev_score}"
            )
            board.render()

            move = self.method(self, board)

            if not board.step(move):
                break

            self.turns += 1

            sleep(0.01)
