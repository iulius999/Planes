import unittest

from src.board.board import Board


class TestBoard(unittest.TestCase):

    def test_init(self):
        b = Board()
        for i in range(10):
            for j in range(10):
                self.assertEqual(b.get_symbol(i, j), '.')

    def test_set(self):
        b = Board()

        b.set_symbol(3, 4, '*')
        self.assertEqual(b.get_symbol(3, 4), '*')

        b.set_symbol(5, 6, '^')
        self.assertEqual(b.get_symbol(5, 6), '^')

    def test_on_board(self):
        b = Board()
        for i in range(10):
            for j in range(10):
                self.assertEqual(b.on_board(i, j), True)

        self.assertEqual(b.on_board(-1, 0), False)
        self.assertEqual(b.on_board(10, 9), False)
