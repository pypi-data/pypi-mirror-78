"""Fixtures for pytest."""

import pytest
from nerdchess.board import Board
from nerdchess import pieces


@pytest.fixture
def board_fixt():
    """Wrap the boardfixt class as a pytest fixture."""
    return BoardFixt(Board())


class BoardFixt():
    """Helper functions to manipulate a board passed as fixture."""

    def __init__(self, board):
        """Init."""
        self.board = board

    def place_piece(self, piece, position):
        """Place a piece or pawn on the board."""
        letter = position[0]
        number = int(position[1])
        self.board.squares[letter][number].occupant = piece
        piece.position = position

    def default_setup(self):
        """Set the board in default game start position.

        Returns:
            board: The new board object
        """
        boardpieces = pieces.create_pieces()
        pawns = pieces.create_pawns()
        self.board.setup_board(boardpieces, pawns)
        return self.board
