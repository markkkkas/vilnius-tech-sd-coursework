import unittest

from models.tile import Tile
from models.checker import Checker
from models.game import Game


class TestInitial(unittest.TestCase):
    def test_checker_removed_none(self):
        tile = Tile(1, 1, "color")
        self.assertEqual(tile.remove_checker(), None)

    def test_checker_removed_existing(self):
        tile = Tile(1, 1, "color")
        checker = Checker(1, 1, "color")

        tile.add_checker(checker)

        self.assertEqual(tile.remove_checker(), checker)

    def test_checker_coords(self):
        checker = Checker(1, 1, "color")
        row, col = checker.get_coords()

        self.assertEqual(checker.get_coords(), (1, 1))

    def test_check_turn(self):
        game = Game(1, 1)

        game.set_next_turn()

        self.assertEqual(game.turn, 1)


if __name__ == "__main__":
    print("tests")
