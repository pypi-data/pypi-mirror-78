"""This module represents a board in a game of chess."""
import copy
from nerdchess.config import colors, letters
from nerdchess.boardmove import BoardMove, CastleSide
from nerdchess.pieces import King


class Board():
    """Represents a board in a game of chess.

    {
        a: {
            1: (Square),
            2: (Square),
            etc...
        },
        b: {
            1: (Square),
            2: (Square),
            etc...
        }
        etc...
    }

    Attributes:
        letters(list): The letters of a board
        numbers(list): The numbers of a board
        squares(dict): A dict of letters containing numbers with squares
    """

    def __init__(self):
        """Init."""
        self.letters = [i.value for i in letters]
        self.numbers = range(1, 9)
        self.squares = {}
        self.__create_board()

    @classmethod
    def piece_list(cls, square_dict, color=None):
        """Generate the current pieces on the board as a list.

        Parameters:
            square_dict(dict): The dictionary of squares to get the list from.
            color(Color): Optional: The color to get the pieces for.

        Yields:
            Piece: A chess piece or pawn
        """
        for v in square_dict.values():
            if isinstance(v, dict):
                yield from cls.piece_list(v, color)
            else:
                if v.occupant:
                    if color:
                        if v.occupant.color == color:
                            yield v.occupant
                        else:
                            pass
                    else:
                        yield v.occupant
                else:
                    pass

    def matrix(self):
        """Return a matrix of the board represented as a nested list."""
        matrix = []

        for i in reversed(self.numbers):
            row = []
            row.append(str(i))

            for letter in self.letters:
                row.append(str(self.squares[letter][i]))

            matrix.append(row)

        last_row = []
        last_row.append(' X ')
        for letter in self.letters:
            last_row.append("_{}_".format(letter))

        matrix.append(last_row)

        return matrix

    def setup_board(self, game_pieces, pawns):
        """Set up the pieces and pawns at their startpositions.

        The lists passed can be created first with
        nerdchess.pieces.create_pieces and nerdchess.pieces.create_pawns.

        Parameters:
            game_pieces(list(Piece)): A list of game pieces to set up
            pawns(list(Pawns)): A list of pawns to set up
        """
        self.__setup_pieces(game_pieces)
        self.__setup_pawns(pawns)

    def __setup_pieces(self, game_pieces):
        """Set up the pieces at their startposition on the board.

        Parameters:
            game_pieces(list(Piece)): A list of pieces to set up
        """
        for piece in game_pieces:
            row = 1 if piece.color == colors.WHITE else 8

            for letter in self.letters:
                square = self.squares[letter][row]
                if (square.selector in piece.start_position()
                        and not square.occupant):
                    piece.position = square.selector
                    square.occupant = piece
                    break

    def __setup_pawns(self, pawns):
        """Set up the pawns on the board.

        Parameters:
            pawns(list(Pawn)): A list of pawns to set up
        """
        for pawn in pawns:
            row = 2 if pawn.color == colors.WHITE else 7

            for letter in self.letters:
                square = self.squares[letter][row]

                if not square.occupant:
                    square.occupant = pawn
                    pawn.position = square.selector
                    break

    def __create_board(self):
        """Create the dict of squares representing the board."""
        for letter in self.letters:
            self.squares[letter] = {}

            for number in self.numbers:
                selector = "{}{}".format(letter, number)
                self.squares[letter][number] = Square(selector)

    def is_check(self, color=None):
        """Is one of the kings in check.

        Parameters:
            color(optional): The color to check for

        Returns:
            color: The color of the king that is in check or False
        """
        pieces = list(self.piece_list(self.squares, color))
        for piece in pieces:
            moves = [BoardMove(self, i.text) for i in piece.allowed_moves()]
            for move in moves:
                if not move:
                    continue

                if not move.destination_sq.occupant:
                    continue

                if (isinstance(move.destination_sq.occupant, King) and
                        move.destination_sq.occupant.color != move.origin_sq.
                        occupant.color):
                    return move.destination_sq.occupant.color

        return False

    def is_checkmate(self):
        """Is one of the kings in checkmate.

        Returns:
            color: Color of the king in mate or False
        """
        check = self.is_check()
        if not check:
            return False

        pieces = list(self.piece_list(self.squares, check))
        moves = []
        for i in pieces:
            moves = moves + i.allowed_moves()

        boardmoves = [BoardMove(self, i.text) for i in moves]

        for move in boardmoves:
            valid_move = move.process()
            if valid_move:
                if not valid_move.is_check(check):
                    return False

        return check

    def new_board(self, move):
        """Create a new board from a supplied move.

        This does not do any explicit validation on the move.
        It does set a piece's captured status to True when needed.
        It does set a piece's new position.

        Parameters:
            move(Move): The move to process

        Returns:
            newboard: The new board
        """
        newboard = copy.deepcopy(self)
        move = BoardMove(newboard, move.text)

        piece = move.origin_sq.occupant

        move.origin_sq.occupant = None
        if move.destination_sq.occupant:
            move.destination_sq.occupant.captured = True
        move.destination_sq.occupant = piece
        piece.position = move.destination_sq.selector

        return newboard

    def castle(self, side, color):
        """Perform castling on a board.

        Parameters:
            side(CastleSide): The side to castle to
            color(Color): The color performing the castle

        Returns:
            newboard: A new board with the processed move
        """
        newboard = copy.deepcopy(self)

        if color == colors.WHITE:
            kingsquare = newboard.squares['e'][1]
            if side == CastleSide.QUEEN:
                rooksquare = newboard.squares['a'][1]
            else:
                rooksquare = newboard.squares['h'][1]
        else:
            kingsquare = newboard.squares['e'][8]
            if side == CastleSide.QUEEN:
                rooksquare = newboard.squares['a'][8]
            else:
                rooksquare = newboard.squares['h'][8]

        kchar = 'c' if side == CastleSide.QUEEN else 'g'
        rchar = 'd' if side == CastleSide.QUEEN else 'f'
        kint = 1 if color == colors.WHITE else 8
        rint = 1 if color == colors.WHITE else 8
        king_dest = newboard.squares[kchar][kint]
        rook_dest = newboard.squares[rchar][rint]

        king = kingsquare.occupant
        rook = rooksquare.occupant
        kingsquare.occupant = None
        rooksquare.occupant = None

        king_dest.occupant = king
        rook_dest.occupant = rook
        king.position = king_dest.selector
        rook.position = rook_dest.selector

        return newboard


class Square():
    """Represents a square on a chessboard.

    Parameters:
        selector(String): A selector of the square (eg. a1)
        occupant(Piece): Usually a piece or pawn, needs to implement __str__

    Attributes:
        selector(String): A selector of the square (eg. a1)
        occupant(Piece): Usually a piece or pawn, needs to implement __str__
    """

    def __init__(self, selector, occupant=None):
        """Init."""
        self.selector = selector
        self.occupant = occupant

    def __str__(self):
        """Text representation of a square.

        Returns:
            String: Either a square filled with the contents of the occupant or
            an empty one.
        """
        if self.occupant:
            return "[{}]".format(str(self.occupant))
        else:
            return '[ ]'
