"""This module describes what pieces and pawns look like."""
from abc import ABC, abstractmethod
from nerdchess.config import colors, numbers, letterlist
from nerdchess.move import Move


class Piece(ABC):
    """Baseclass of a game piece (pawns and pieces).

    Parameters:
        color(colors): The color of the piece
        captured(Bool): Is the piece captured?

    Attributes:
        color(colors): The color of the piece
        position(String): The position of the piece
        captured(Bool): Is the piece captured?
    """

    def __init__(self, color, captured=False):
        """Init."""
        self.color = color
        self.position = ''
        self.captured = captured

    @abstractmethod
    def start_position(self):
        """Start positions of a piece."""
        pass

    @abstractmethod
    def move_pattern(self):
        """Movevement pattern of a piece.

        Returns:
            list(tuple(int, int), ): Move pattern as list of tuples
        """
        pass

    def diagonal_pattern(self):
        """Return a diagonal movement pattern as a list (bishops)."""
        pattern = []
        cur_letter = self.position[0]
        pos_letter = letterlist.index(cur_letter)

        for letter in letterlist:
            letter_diff = letterlist.index(letter) - pos_letter
            pattern.append((0 + letter_diff, letter_diff))
            pattern.append((0 - letter_diff, letter_diff))
            pattern.append((letter_diff, 0 + letter_diff))
            pattern.append((letter_diff, 0 - letter_diff))

        return pattern

    def straight_pattern(self):
        """Return a straight movement pattern as a list (rooks)."""
        pattern = []
        cur_letter = self.position[0]
        cur_number = int(self.position[1])
        pos_letter = letterlist.index(cur_letter)
        pos_number = numbers.index(cur_number)

        for letter in letterlist:
            letter_diff = letterlist.index(letter) - pos_letter
            pattern.append((letter_diff, 0))
        for number in numbers:
            number_diff = numbers.index(number) - pos_number
            pattern.append((0, number_diff))

        return pattern

    def allowed_moves(self):
        """Transform the move pattern into a list of allowed moves.

        Returns:
            list(Move, ): A list of allowed moves for the piece
                          doesn't factor in other pieces on the board.
        """
        allowed_moves = []
        for move in self.move_pattern():
            try:
                new_move = Move.from_position(self.position, move)
                if new_move:
                    allowed_moves.append(new_move)
            except IndexError:
                pass

        return allowed_moves

    @abstractmethod
    def __str__(self):
        """Text representation of the class."""
        pass

    def __eq__(self, item):
        """Compare this class."""
        if type(item) == type(self):
            return self.color == item.color
        else:
            return NotImplemented


class Pawn(Piece):
    """Represents a pawn in a game of chess."""

    def __str__(self):
        """Text representation of the class."""
        if self.color == colors.BLACK:
            return u'\u2659'
        else:
            return u'\u265F'

    def start_position(self):
        """Start positions of a piece."""
        pass

    def move_pattern(self):
        """Movevement pattern of a piece.

        Returns:
            list(tuple(int, int), ): Move pattern as list of tuples
        """
        pattern = []

        if self.color == colors.WHITE:
            pattern.append((0, 1))
            pattern.append((-1, 1))
            pattern.append((1, 1))
            if int(self.position[1]) == 2:
                pattern.append((0, 2))
        else:
            pattern.append((0, -1))
            pattern.append((1, -1))
            pattern.append((-1, -1))
            if int(self.position[1]) == 7:
                pattern.append((0, -2))

        return pattern


class Rook(Piece):
    """Represents a rook in a game of chess."""

    def __str__(self):
        """Text representation of the class."""
        if self.color == colors.BLACK:
            return u'\u2656'
        else:
            return u'\u265C'

    def start_position(self):
        """Start positions of a piece."""
        if self.color == colors.BLACK:
            return ('a8', 'h8')
        else:
            return ('a1', 'h1')

    def move_pattern(self):
        """Movevement pattern of a piece.

        Returns:
            list(tuple(int, int), ): Move pattern as list of tuples
        """
        return self.straight_pattern()


class Bishop(Piece):
    """Represents a bishop in a game of chess."""

    def __str__(self):
        """Text representation of the class."""
        if self.color == colors.BLACK:
            return u'\u2657'
        else:
            return u'\u265D'

    def start_position(self):
        """Start positions of a piece."""
        if self.color == colors.BLACK:
            return ('c8', 'f8')
        else:
            return ('c1', 'f1')

    def move_pattern(self):
        """Movevement pattern of a piece.

        Returns:
            list(tuple(int, int), ): Move pattern as list of tuples
        """
        return self.diagonal_pattern()


class Knight(Piece):
    """Represents a knight in a game of chess."""

    def __str__(self):
        """Text representation of the class."""
        if self.color == colors.BLACK:
            return u'\u2658'
        else:
            return u'\u265E'

    def start_position(self):
        """Start positions of a piece."""
        if self.color == colors.BLACK:
            return ('b8', 'g8')
        else:
            return ('b1', 'g1')

    def move_pattern(self):
        """Movevement pattern of a piece.

        Returns:
            list(tuple(int, int), ): Move pattern as list of tuples
        """
        pattern = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2)
        ]
        return pattern


class Queen(Piece):
    """Represents a queen in a game of chess."""

    def __str__(self):
        """Text representation of the class."""
        if self.color == colors.BLACK:
            return u'\u2655'
        else:
            return u'\u265B'

    def start_position(self):
        """Start positions of a piece."""
        if self.color == colors.BLACK:
            return 'd8'
        else:
            return 'd1'

    def move_pattern(self):
        """Movevement pattern of a piece.

        Returns:
            list(tuple(int, int), ): Move pattern as list of tuples
        """
        straight = self.straight_pattern()
        diagonal = self.diagonal_pattern()
        pattern = straight + diagonal
        return pattern


class King(Piece):
    """Represents a king in a game of chess."""

    def __str__(self):
        """Text representation of the class."""
        if self.color == colors.BLACK:
            return u'\u2654'
        else:
            return u'\u265A'

    def start_position(self):
        """Start positions of a piece."""
        if self.color == colors.BLACK:
            return 'e8'
        else:
            return 'e1'

    def move_pattern(self):
        """Movevement pattern of a piece.

        Returns:
            list(tuple(int, int), ): Move pattern as list of tuples
        """
        pattern = [
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (1, 0),
            (-1, 1),
            (-1, 0),
            (-1, -1)
        ]

        if self.position == self.start_position():
            pattern.append((2, 0))
            pattern.append((3, 0))
            pattern.append((-2, 0))
            pattern.append((-3, 0))
            pattern.append((-4, 0))

        return pattern


def create_pieces():
    """Create a standard set of chess pieces."""
    chess_pieces = []

    for color in colors:
        chess_pieces.append(Rook(color))
        chess_pieces.append(Rook(color))
        chess_pieces.append(Knight(color))
        chess_pieces.append(Knight(color))
        chess_pieces.append(Bishop(color))
        chess_pieces.append(Bishop(color))
        chess_pieces.append(Queen(color))
        chess_pieces.append(King(color))

    return chess_pieces


def create_pawns():
    """Create a standard set of pawns."""
    pawns = []

    for color in colors:
        for letter in letterlist:
            pawns.append(Pawn(color))

    return pawns
