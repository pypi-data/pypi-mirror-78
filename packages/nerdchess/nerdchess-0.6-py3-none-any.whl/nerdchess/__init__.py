"""A chess engine written in Python.

The goal of this project is to offer simple tools to simulate a game of chess,
by offering the necessary objects like a board, pieces, pawns and players
standalone. But also a complete chessgame that implements these objects
and offers an interface to control the game.

The package includes a small commandline chess game, but the main goal is to
offer an interface to create chess games from everywhere. It should be just as
easy to implement the same games of chess in a web-application with Flask, a
commandline interface or some graphical desktop interface.

It's still the idea to make it possible to write AI's againt this package.
But for now I'm just going to finish it's basic functionality and try to keep
it in mind as much as I can while making design decisions.

I'm not aiming for this to be some widely used package, and am mostly making it
for fun and learning. Expect things to change a lot, and your applications to
break if you don't freeze versions might you decide to use this. At least in
it's current state.
"""
from nerdchess import game
from nerdchess.player import Player
from tabulate import tabulate


def main():
    """Play a game of chess.

    The main function of this module starts a really basic game of chess on the
    commandline. Moves are input in the format 'e2e4'.

    Examples:
        >>> import nerdchess
        >>> nerdchess.main()
        What is the name of player 1?henk
        With which color should henk start, (w)hite, (b)lack or (r)andom?     r
        What is the name of player 2?blaat
        -  ---  ---  ---  ---  ---  ---  ---  ---
        8  [♖]  [♘]  [♗]  [♕]  [♔]  [♗]  [♘]  [♖]
        7  [♙]  [♙]  [♙]  [♙]  [♙]  [♙]  [♙]  [♙]
        6  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]
        5  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]
        4  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]
        3  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]
        2  [♟]  [♟]  [♟]  [♟]  [♟]  [♟]  [♟]  [♟]
        1  [♜]  [♞]  [♝]  [♛]  [♚]  [♝]  [♞]  [♜]
        X  _a_  _b_  _c_  _d_  _e_  _f_  _g_  _h_
        -  ---  ---  ---  ---  ---  ---  ---  ---
        What's your move, blaat?: e2e4
        -  ---  ---  ---  ---  ---  ---  ---  ---
        8  [♖]  [♘]  [♗]  [♕]  [♔]  [♗]  [♘]  [♖]
        7  [♙]  [♙]  [♙]  [♙]  [♙]  [♙]  [♙]  [♙]
        6  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]
        5  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]
        4  [ ]  [ ]  [ ]  [ ]  [♟]  [ ]  [ ]  [ ]
        3  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]  [ ]
        2  [♟]  [♟]  [♟]  [♟]  [ ]  [♟]  [♟]  [♟]
        1  [♜]  [♞]  [♝]  [♛]  [♚]  [♝]  [♞]  [♜]
        X  _a_  _b_  _c_  _d_  _e_  _f_  _g_  _h_
        -  ---  ---  ---  ---  ---  ---  ---  ---
    """
    name_1 = input('What is the name of player 1?')
    name_1_color = input(
        "With which color should {} start, (w)hite, (b)lack or (r)andom?\
        ".format(name_1))
    name_2 = input('What is the name of player 2?')

    (player_1,
     player_2) = Player.create_two(name_1, name_2, name_1_color)
    chessgame = game.ChessGame(player_1, player_2)

    print(tabulate(chessgame.board.matrix()))

    while not chessgame.over:
        for player in chessgame.playerlist:
            if player.turn:
                current_player = player

        if not player:
            raise ValueError(
                'Player not found, something has gone horribly wrong.')

        move = input("What's your move, {}?: ".format(current_player.name))
        chessgame.move(current_player, move)

        print(tabulate(chessgame.board.matrix()))


if __name__ == '__main__':
    main()
