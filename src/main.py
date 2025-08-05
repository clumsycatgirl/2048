import getpass
from collections import Counter
from random import random, randrange
from typing import List, Tuple

from .g2048 import solvers
from .g2048.board import Board
from .g2048.solver import Solver
from .utils.cli import cls

"""
    |---------------|
0   |   |   |   |   |
1   |   |   |   |   |
2   |   |   |   |   |
3   |   |   |   |   |
Y   |---------------|
  X  0   1   2   3 
"""


def main() -> None:
    board: Board = Board(4, 4)

    num_of_blocks = randrange(1, 4)
    for i in range(num_of_blocks):
        x, y = randrange(0, board.width), randrange(0, board.height)
        board[(x, y)] = 4 if random() > 0.7 else 2

    solver = Solver("cbs", solvers.closest_best_simple)
    while not board.full():
        cls()
        board.render()

        move = getpass.getpass("")

        allowed = ["up", "down", "left", "right"]
        short = ["w", "s", "a", "d"]
        if move not in allowed and move not in short:
            continue

        board.step(move)

    print("\n---game over---")


def auto() -> None:
    scores: List[Tuple[float, int, str]] = []

    NUMBER_OF_ITERATIONS: int = 10

    methods = [
        # ("up-left", solvers.up_left),
        # ("down-right", solvers.down_right),
        # ("random", solvers.random),
        # ("circular", solvers.circular),
        # ("closest_best_simple", solvers.closest_best_simple),
        # ("closest_best_circular", solvers.closest_best_circular),
        # ("look_ahead_simple", solvers.look_ahead_simple),
        # ("look_ahead_position_aware", solvers.look_ahead_position_aware),
        ("expectimax", solvers.expectimax),
    ]

    try:
        for method in methods:
            print(f"{method=}")
            for n in range(NUMBER_OF_ITERATIONS):
                board: Board = Board(4, 4)

                num_of_blocks = randrange(1, 4)
                for i in range(num_of_blocks):
                    x, y = randrange(0, board.width), randrange(0, board.height)
                    board[(x, y)] = 4 if random() > 0.7 else 2

                solver = Solver(method_name=method[0], method=method[1])

                solver.solve(
                    board=board,
                    iteration=n,
                    prev_score=(scores[-1] if len(scores) > 0 else (0, 0, "")),
                    max_score=(max(scores) if len(scores) > 0 else (0, 0, "")),
                )

                scores.append((board.score(), solver.turns, method[0]))
    except AssertionError as e:
        print(e)
    except KeyboardInterrupt:
        print("---simulation stopped---")
        pass

    print("\n---simulation done---")
    if len(scores) > 0:
        print(f"max_score={max(scores)}")
    print("scores")
    final_scores = Counter(scores)
    for score in reversed(sorted(final_scores)):
        print(f"\tmethod='{score[2]}'\t\tscore={score[0]}\tturns={score[1]}")
