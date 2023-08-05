"""Init for nerdchess.

When ran standalone opens a small TUI game of chess.
"""
from nerdchess import game
from nerdchess.player import Player
from tabulate import tabulate


def main():
    """Play a gane of chess."""
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
