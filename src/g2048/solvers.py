import math
from copy import deepcopy
from random import randrange
from typing import Tuple

from ..utils.decorators import static_vars
from .board import Board
from .solver import Solver


def up_left(solver: Solver, board: Board) -> str:
    up = solver.turns % 2 == 0
    return "w" if up else "a"


def down_right(solver: Solver, board: Board) -> str:
    up = solver.turns % 2 == 0
    return "s" if up else "d"


def random(solver: Solver, board: Board) -> str:
    match (randrange(0, 4)):
        case 0:
            return "w"
        case 1:
            return "a"
        case 2:
            return "s"
        case 3:
            return "d"
    return "unreachable"


def circular(solver: Solver, board: Board) -> str:
    remainder = solver.turns % 4
    match (remainder):
        case 0:
            return "w"
        case 1:
            return "a"
        case 2:
            return "s"
        case 3:
            return "d"
    return "unreachable"


def closest_best_simple(solver: Solver, board: Board) -> str:
    def score_position(board: Board) -> float:
        score: float = 0
        for row in board:
            for cell in row:
                if cell == 0:
                    continue
                score += cell * math.log2(cell)
        return score

    def test_move(move: str) -> Tuple[float, str]:
        b = deepcopy(board)
        b.step(move)
        return (score_position(b), move)

    score_up, score_left, score_down, score_right = (
        test_move("w"),
        test_move("a"),
        test_move("s"),
        test_move("d"),
    )
    move = max(score_up, score_left, score_down, score_right)[1]

    if score_up == score_left and score_left == score_right and score_right == score_up:
        move = ["w", "a", "s", "d"][randrange(0, 4)]

    return move


@static_vars(last_move=None)
def closest_best_circular(solver: Solver, board: Board) -> str:
    def score_position(board: Board) -> float:
        score: float = 0
        for row in board:
            for cell in row:
                if cell == 0:
                    continue
                score += cell * math.log2(cell)
        return score

    def test_move(move: str) -> Tuple[float, str]:
        b = deepcopy(board)
        b.step(move)
        return (score_position(b), move)

    score_up, score_left, score_down, score_right = (
        test_move("w"),
        test_move("a"),
        test_move("s"),
        test_move("d"),
    )
    move = max(score_up, score_left, score_down, score_right)[1]

    if score_up == score_left and score_left == score_right and score_right == score_up:
        moves = ["w", "a", "s", "d"]
        current_index = (
            moves.index(closest_best_circular.last_move)
            if closest_best_circular.last_move is not None
            else 0
        )
        current_index = (current_index + 1) % 4
        move = moves[current_index]

    closest_best_circular.last_move = move
    return move


@static_vars(last_move=None)
def look_ahead_simple(solver: Solver, board: Board) -> str:
    def score_position(board: Board) -> float:
        score: float = 0
        for x in range(board.width):
            for y in range(board.height):
                cell = board[(x, y)]
                if cell == 0:
                    continue
                score += cell * math.log2(cell)
        return score

    def test_move(move: str, board: Board, depth: int = 2) -> Tuple[float, str]:
        if depth == 0:
            return (0, "")

        b = deepcopy(board)
        b.step(move)
        position_score = score_position(b)
        position_score += test_move("w", b, depth - 1)[0]
        position_score += test_move("a", b, depth - 1)[0]
        position_score += test_move("s", b, depth - 1)[0]
        position_score += test_move("d", b, depth - 1)[0]

        return (position_score, move)

    score_up, score_left, score_down, score_right = (
        test_move("w", board, 4),
        test_move("a", board, 4),
        test_move("s", board, 4),
        test_move("d", board, 4),
    )

    move = max(score_up, score_left, score_down, score_right)[1]

    if score_up == score_left and score_left == score_right and score_right == score_up:
        moves = ["w", "a", "s", "d"]
        current_index = (
            moves.index(look_ahead_simple.last_move)
            if look_ahead_simple.last_move is not None
            else 0
        )
        current_index = (current_index + 1) % 4
        move = moves[current_index]

    look_ahead_simple.last_move = move
    return move


@static_vars(last_move=None)
def look_ahead_space_conscious(solver: Solver, board: Board) -> str:
    def score_position(board: Board) -> float:
        score: float = 0
        for x in range(board.width):
            for y in range(board.height):
                cell = board[(x, y)]
                if cell == 0:
                    continue
                score += cell * math.log2(cell)
        return score

    def test_move(move: str, board: Board, depth: int = 2) -> Tuple[float, str]:
        if depth == 0:
            return (0, "")

        b = deepcopy(board)
        b.step(move)
        position_score = score_position(b)
        position_score += test_move("w", b, depth - 1)[0]
        position_score += test_move("a", b, depth - 1)[0]
        position_score += test_move("s", b, depth - 1)[0]
        position_score += test_move("d", b, depth - 1)[0]

        return (position_score, move)

    score_up, score_left, score_down, score_right = (
        test_move("w", board, 2),
        test_move("a", board, 2),
        test_move("s", board, 2),
        test_move("d", board, 2),
    )

    move = max(score_up, score_left, score_down, score_right)[1]

    if score_up == score_left and score_left == score_right and score_right == score_up:
        moves = ["w", "a", "s", "d"]
        current_index = (
            moves.index(look_ahead_space_conscious.last_move)
            if look_ahead_space_conscious.last_move is not None
            else 0
        )
        current_index = (current_index + 1) % 4
        move = moves[current_index]

    look_ahead_space_conscious.last_move = move
    return move
