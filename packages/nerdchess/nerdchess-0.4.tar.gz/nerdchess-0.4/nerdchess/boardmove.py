"""A move in the context of a board.

This module glues moves and a board together.
"""
from nerdchess import pieces
from nerdchess.move import Move
from nerdchess.config import colors
from nerdchess.boardrules import BoardRules
from enum import Enum


class CastleSide(Enum):
    """Enumerator with castling sides."""

    QUEEN = 'queenside'
    KING = 'kingside'


class BoardMove(Move):
    """Represents a move in the context of a board.

    Inherits base class (Move) attributes.
    And adds some new ones.

    Parameters:
        board(Board): The board we're playing on.

    Attributes:
        board(Board): The boardcontext.
        origin_sq(Square): The origin square.
        destination_sq(Square): The destination square.
    """

    def __init__(self, board, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.board = board
        (self.origin_sq,
         self.destination_sq) = self.__get_origin_destination()

    def castle_side(self):
        """Return the side we're castling to."""
        castling = self.is_castling()
        if not castling:
            raise Exception('Trying to determine castleside but not castling.')

        if self.horizontal > 0:
            return CastleSide.KING
        else:
            return CastleSide.QUEEN

    def is_capturing(self):
        """Is this a capturing move."""
        if self.destination_sq.occupant:
            return True
        else:
            return False

    def is_castling(self):
        """Is this a castling move."""
        piece = self.origin_sq.occupant
        is_king = isinstance(piece, pieces.King)
        is_rook = isinstance(piece, pieces.Rook)
        castling_moves = [
            Move('e1g1'),
            Move('e1h1'),
            Move('e1c1'),
            Move('e1b1'),
            Move('e1a1'),
            Move('h1e1'),
            Move('a1e1'),
            Move('e8g8'),
            Move('e8h8'),
            Move('e8c8'),
            Move('e8b8'),
            Move('e8a8'),
            Move('h8e8'),
            Move('a8e8')
        ]

        if not is_king and not is_rook:
            return False

        if piece.color == colors.WHITE:
            king = pieces.King(colors.WHITE)
            if self.board.squares['e'][1].occupant != king:
                return False
        else:
            king = pieces.King(colors.BLACK)
            if self.board.squares['e'][8].occupant != king:
                return False

        if self not in castling_moves:
            return False

        return piece.color

    def __get_origin_destination(self):
        """Get the origin and destination square of a move.

        Returns:
            tuple(Square, Square): The origin and destination
        """
        o_letter = str(self.origin[0])
        o_number = int(self.origin[1])

        d_letter = str(self.destination[0])
        d_number = int(self.destination[1])

        origin = self.board.squares[o_letter][o_number]
        destination = self.board.squares[d_letter][d_number]

        return (origin, destination)

    def process(self):
        """Process a move in the context of the board.

        Returns:
            Bool: False if the move is incorrect
            Board: A new board
        """
        piece = self.origin_sq.occupant

        if self.origin_sq == self.destination_sq:
            return False

        if not piece:
            return False

        if Move(self.text) not in piece.allowed_moves():
            return False

        boardrules = BoardRules(self)
        if not boardrules.valid:
            return False

        castling = self.is_castling()
        if not castling:
            newboard = self.board.new_board(self)
        else:
            side = self.castle_side()
            newboard = self.board.castle(side, piece.color)

        if newboard.is_check() == piece.color:
            return False

        return newboard
