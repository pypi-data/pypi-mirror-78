"""Global config for nerdchess.

Attributes:
    MOVE_REGEX (Regex): Regex to validate a move.
    numbers (list(int)): List of numbers of a chessboard.
    letterlijst (list(letter(Enum))): List of letters of a chessboard.
"""
from enum import Enum
import re


class colors(Enum):
    """The colors of the players in a game of chess."""

    WHITE = 'w'
    BLACK = 'b'


class letters(Enum):
    """The letters of a chess board."""

    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'


MOVE_REGEX = re.compile(r"[a-h][1-8][a-h][1-8]")
numbers = range(1, 9)
letterlist = [i.value for i in letters]
