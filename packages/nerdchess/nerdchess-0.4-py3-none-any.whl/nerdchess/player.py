"""Represent a player in a game of chess."""
import random
from nerdchess.config import colors


def random_color():
    """Return a random color."""
    if bool(random.getrandbits(1)):
        return colors.WHITE
    else:
        return colors.BLACK


class Player():
    """Represents a player in a chessgame.

    Args:
        name: The name of the player
        color: The color of the player
        turn: Whether it's the players turn

    Attributes:
        name: The name of the player
        color: The color of the player
        turn: Is it the players turn?
    """

    def __init__(self, name, color, turn=True, *args, **kwargs):
        """Init."""
        self.name = name
        self.color = color
        self.turn = turn

    def __str__(self):
        """Text representation of a player."""
        return "{}, playing {}.".format(self.name, self.color)

    @classmethod
    def create_two(cls, name_1, name_2, color_input):
        """Create two players and base the colors off of the one assigned to 1.

        Parameters:
            name_1: The name of player 1
            name_2: The name of player 2
            color_input: The color to assign to player 1

        Returns:
            Tuple(Player, Player): The players that are going to play the game
        """
        if color_input == 'r':
            color = random_color()
            turn = True if color == colors.WHITE else False
            player_1 = Player(name_1, color, turn)
        elif color_input == colors.WHITE.value:
            player_1 = Player(name_1, colors.WHITE)
        elif color_input == colors.BLACK.value:
            player_1 = Player(name_1, colors.BLACK, False)
        else:
            raise ValueError('Wrong color input.')

        player_2_color = (colors.WHITE if player_1.color == colors.BLACK
                          else colors.BLACK)

        turn = True if player_2_color == colors.WHITE else False
        player_2 = Player(name_2, player_2_color, turn)

        return (player_1, player_2)
