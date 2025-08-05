import math
from copy import deepcopy
from random import randrange, choice
from typing import Tuple, Optional, List
from functools import wraps

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
def look_ahead_position_aware(solver: Solver, board: Board) -> str:
    def score_position(board: Board) -> float:
        score = 0
        largest_tile = max([cell for row in board._data for cell in row if cell > 0], default=0)

        for x in range(board.width):
            for y in range(board.height):
                cell = board[(x, y)]
                if cell == 0:
                    continue

                score += cell * math.log2(cell)

                if (x, y) == (0, board.height - 1): 
                    score += 5 * math.log2(cell)  
                if (x, y) == (board.width - 1, board.height - 1):
                    score += 5 * math.log2(cell) 

                if (x, y) not in [(0, 0), (0, board.height - 1), (board.width - 1, 0), (board.width - 1, board.height - 1)]:
                    score -= 0.2 * cell 

                if x < board.width - 1 and board[(x + 1, y)] == cell:
                    score += 2 
                if y < board.height - 1 and board[(x, y + 1)] == cell:
                    score += 2 

                if largest_tile > 0 and abs(x - 3) + abs(y - 0) <= 2: 
                    score += 0.5 * cell
                if largest_tile > 0 and abs(x - 3) + abs(y - 3) <= 2: 
                    score += 0.5 * cell

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
            moves.index(look_ahead_position_aware.last_move)
            if look_ahead_position_aware.last_move is not None
            else 0
        )
        current_index = (current_index + 1) % 4 
        move = moves[current_index]

    look_ahead_position_aware.last_move = move
    return move

def expectimax(solver: Solver, board: Board) -> str:
    MAX_DEPTH = 3

    def score_board(b: Board) -> float:
        empty_cells = sum(1 for x in range(b.width) for y in range(b.height) if b[(x, y)] == 0)
        max_tile = max(cell for row in b._data for cell in row)
        smoothness = 0

        for x in range(b.width):
            for y in range(b.height):
                value = b[(x, y)]
                if value == 0:
                    continue
                for dx, dy in [(1, 0), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if nx < b.width and ny < b.height and b[(nx, ny)] != 0:
                        smoothness -= abs(value - b[(nx, ny)])

        return (
            empty_cells * 100
            + math.log2(max_tile) * 10
            + smoothness * 0.5
        )

    def get_children_after_move(b: Board, move: str) -> Optional[Board]:
        new_b = deepcopy(b)
        if new_b.step(move):
            return new_b
        return None

    def get_all_random_children(b: Board) -> List[Tuple[Board, float]]:
        children = []
        for x in range(b.width):
            for y in range(b.height):
                if b[(x, y)] == 0:
                    for value, prob in [(2, 0.9), (4, 0.1)]:
                        child = deepcopy(b)
                        child._data[y][x] = value
                        children.append((child, prob))
        return children

    def expectimax_value(b: Board, depth: int, is_player_turn: bool) -> float:
        if depth == 0:
            return score_board(b)

        if is_player_turn:
            max_value = float('-inf')
            for move in ['w', 'a', 's', 'd']:
                child = get_children_after_move(b, move)
                if child:
                    value = expectimax_value(child, depth - 1, False)
                    max_value = max(max_value, value)
            return max_value if max_value != float('-inf') else score_board(b)
        else:
            children = get_all_random_children(b)
            if not children:
                return score_board(b)
            total = 0
            for child, prob in children:
                total += prob * expectimax_value(child, depth - 1, True)
            return total / len(children)

    best_score = float('-inf')
    best_move = 'w'
    for move in ['w', 'a', 's', 'd']:
        child = get_children_after_move(board, move)
        if child:
            value = expectimax_value(child, MAX_DEPTH - 1, False)
            if value > best_score:
                best_score = value
                best_move = move

    return best_move
