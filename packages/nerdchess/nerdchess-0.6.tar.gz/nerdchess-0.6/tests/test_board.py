import pytest
from nerdchess.pieces import King, Queen, Bishop
from nerdchess.config import colors


class TestBoard():
    """ Test aspects of the Board class. """

    @pytest.mark.parametrize("king_pos,expected", [
        ('e5', colors.BLACK),
        ('f6', False),
    ])
    def test_ischeck(self, board_fixt, king_pos, expected):
        """ Test if kingcheck works correctly """
        board_fixt.place_piece(Queen(colors.WHITE), 'e4')
        board_fixt.place_piece(King(colors.BLACK), king_pos)
        check = board_fixt.board.is_check()

        assert check == expected

    @pytest.mark.parametrize("king_pos,expected", [
        ('h1', colors.WHITE),
        ('f3', False),
    ])
    def test_checkmate(self, board_fixt, king_pos, expected):
        board_fixt.place_piece(Queen(colors.BLACK), 'g2')
        board_fixt.place_piece(Bishop(colors.BLACK), 'h3')
        board_fixt.place_piece(King(colors.WHITE), king_pos)
        check = board_fixt.board.is_checkmate()

        assert check == expected
