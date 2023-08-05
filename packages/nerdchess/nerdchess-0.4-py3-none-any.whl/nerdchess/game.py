"""Start a game of chess.

This module offers a simple interface to start a game of chess.
The game consists of:
    - 2 Players
    - A board
    - Pieces
    - Pawns

Example:
    chessgame = game.ChessGame(player_1, player_2)
"""

from nerdchess import pieces
from nerdchess.board import Board
from nerdchess.boardmove import BoardMove


class ChessGame():
    """Creates a new chessgame with players, pieces, and sets up the board.

    Parameters:
        name_1(Player): Player 1
        name_2(Player): Player 2
        over(Bool): Whether the game is over

    Attributes:
        player_1(Player): Player 1
        player_2(Player): Player 2
        playerlist(list): A list of the two players
        board(Board): The board the game is played on
        pieces(list): A list of the pieces the game is played with
        pawns(list): A list of the pawns the game is played with
    """

    def __init__(self, player_1, player_2, over=False):
        """Init."""
        self.player_1 = player_1
        self.player_2 = player_2
        self.playerlist = [self.player_1, self.player_2]

        self.board = Board()
        self.pieces = pieces.create_pieces()
        self.pawns = pieces.create_pawns()
        self.board.setup_board(self.pieces, self.pawns)
        self.over = over

    def pass_turn(self):
        """Pass the turn to the other player."""
        for player in self.playerlist:
            player.turn = False if player.turn else True

    def move(self, player, move):
        """Process the move in a game of chess.

        Parameters:
            player: The player that made the move
            move: The move representeed by squares (eg. e2e4)

        Returns:
            Bool: Was the move succesful?
        """
        move = BoardMove(self.board, move)

        if move.origin_sq.occupant:
            if move.origin_sq.occupant.color != player.color:
                return False
        else:
            return False

        result = move.process()
        if result:
            if result.is_checkmate():
                self.over = True
            self.board = result
            self.pass_turn()
            return True
        else:
            return False
