import getpass
from collections import Counter
from random import random, randrange
from typing import List, Tuple
import os

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

    NUMBER_OF_ITERATIONS: int = 1_000

    methods = [
        ("up-left", solvers.up_left),
        ("down-right", solvers.down_right),
        ("random", solvers.random),
        ("circular", solvers.circular),
        ("closest_best_simple", solvers.closest_best_simple),
        ("closest_best_circular", solvers.closest_best_circular),
        ("look_ahead_simple", solvers.look_ahead_simple),
        ("look_ahead_position_aware", solvers.look_ahead_position_aware),
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
    final_scores = sorted(Counter(final_scores), key=lambda x: (-x[0], x[1]))
    for score in final_scores:
        print(f"\tmethod='{score[2]}'\t\t\tscore={score[0]}\tturns={score[1]}")

    base_filename = "results/simulation_results.txt"
    filename = base_filename
    counter = 1

    while os.path.exists(filename):
        name, ext = os.path.splitext(base_filename)
        filename = f"{name}_{counter}{ext}"
        counter += 1

    with open(filename, "w") as f:
        if len(scores) > 0:
            f.write(f"max_score: method={final_scores[0][2]}, score={final_scores[0][0]}, turns={final_scores[0][1]}\n")
        f.write("scores\n")
        for score in final_scores:
            print(f"\tmethod='{score[2]}'\t\t\tscore={score[0]}\tturns={score[1]}\n")

    print(f"\n---results written to '{filename}'---")
