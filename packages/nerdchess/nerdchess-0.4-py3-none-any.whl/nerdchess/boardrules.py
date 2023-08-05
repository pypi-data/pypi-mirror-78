"""Helps check for valid moves in the context of a board."""

from nerdchess import pieces
from nerdchess.move import Move


class BoardRules():
    """Applies different boardrules.

    Parameters:
        move: The boardmove to check against

    Attributes:
        move: The move we're checking
        valid: Is the checked move valid? see self.apply()
        origin: The origin square of the move
        destination: The destination square of the move
        piece: The piece being moved
    """

    def __init__(self, move):
        """Init."""
        self.move = move
        self.valid = True
        self.piece = self.move.origin_sq.occupant
        self.apply()

    def apply(self):
        """Apply boardrules based on the moved piece."""
        if isinstance(self.piece, pieces.Pawn):
            self.__pawn_rules()
        if not isinstance(self.piece, pieces.Knight):
            self.__blocking_pieces()
        if self.move.is_castling():
            self.__castling()
        else:
            if self.move.is_capturing():
                self.__capturing()
            self.__self_checking()

    def __capturing(self):
        """Check if this is a capturing move."""
        if (self.move.destination_sq.occupant.color ==
                self.move.origin_sq.occupant.color):
            self.valid = False

    def __pawn_rules(self):
        """Rules to apply to pawns only."""
        if self.move.horizontal == 1:
            # If we're going horizontal, are we at least capturing?
            if not self.move.destination_sq.occupant:
                d_letter = self.move.destination[0]
                o_number = int(self.move.origin[1])
                # If not, is it at least en passant?
                if not isinstance(
                        self.move.board.squares[d_letter][o_number].occupant,
                        pieces.Pawn):
                    self.valid = False

    def __blocking_pieces(self):
        """Check if the move is being blocked."""
        for square in self.move.squares_between():
            c = square[0]
            i = int(square[1])
            if self.move.board.squares[c][i].occupant:
                self.valid = False

    def __self_checking(self):
        """Check if the move puts the player itself in check."""
        newboard = self.move.board.new_board(self.move)
        if newboard.is_check() == self.piece.color:
            self.valid = False

    def __castling(self):
        """Apply rules specific to castling."""
        pattern = []

        if self.move.board.is_check() == self.piece.color:
            self.valid = False

        if self.move.horizontal > 0:
            pattern = [
                (1, 0),
                (2, 0)
            ]
        else:
            pattern = [
                (-1, 0),
                (-2, 0)
            ]

        for move in pattern:
            inter_move = Move.from_position(self.piece.position, move)
            inter_board = self.move.board.new_board(inter_move)
            if inter_board.is_check() == self.piece.color:
                self.valid = False
