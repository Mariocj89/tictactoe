import unittest

from tictactoe.board import Board, CIRCLE, CROSS, AlreadySet


class BoardTest(unittest.TestCase):
    def test_no_winner_on_empty(self):
        self.assertFalse(Board().winner)

    def test_first_line_x_winner(self):
        board = Board()
        board.x(0, 0)
        board.x(0, 1)
        board.x(0, 2)
        self.assertEqual(CROSS, board.winner)

    def test_first_line_not_completed_no_winner(self):
        board = Board()
        board.x(0, 0)
        board.x(0, 1)
        self.assertFalse(board.winner)

    def test_first_line_mixed_no_winner(self):
        board = Board()
        board.x(0, 0)
        board.x(0, 1)
        board.o(0, 2)
        self.assertFalse(board.winner)

    def test_first_column_completed_o_winner(self):
        board = Board()
        board.o(0, 0)
        board.o(1, 0)
        board.o(2, 0)
        self.assertEqual(CIRCLE, board.winner)

    def test_first_column_mixed_no_winner(self):
        board = Board()
        board.x(0, 0)
        board.x(1, 0)
        board.o(2, 0)
        self.assertFalse(board.winner)

    def test_diagonal_completed_o_winner(self):
        board = Board()
        board.o(0, 0)
        board.o(1, 1)
        board.o(2, 2)
        self.assertEqual(CIRCLE, board.winner)

    def test_diagonal2_completed_o_winner(self):
        board = Board()
        board.o(0, 2)
        board.o(1, 1)
        board.o(2, 0)
        self.assertEqual(CIRCLE, board.winner)

    def test_diagonal2_not_completed_no_winner(self):
        board = Board()
        board.o(0, 2)
        board.o(1, 1)
        board.x(2, 0)
        self.assertFalse(board.winner)

    def test_empty_not_completed(self):
        self.assertFalse(Board().completed)

    def test_column_not_completed(self):
        board = Board()
        board.o(0, 2)
        board.o(1, 1)
        board.x(2, 0)
        self.assertFalse(board.completed)

    def test_cannot_override_diff_value(self):
        board = Board()
        board.x(0, 2)
        self.assertRaises(AlreadySet, board.o, 0, 2)

    def test_cannot_override_same_value(self):
        board = Board()
        board.o(0, 2)
        self.assertRaises(AlreadySet, board.o, 0, 2)

    def test_full_completed(self):
        board = Board()
        for i in range(3):
            for j in range(3):
                board.o(i, j)
        self.assertTrue(board.completed)

    def test_check_free_on_free_cell(self):
        board = Board()
        board.o(0, 2)
        self.assertTrue(board.is_free(1, 2))

    def test_check_free_on_not_free_cell(self):
        board = Board()
        board.o(0, 2)
        self.assertFalse(board.is_free(0, 2))

    def test_clone_copies_already_set_cells(self):
        board = Board()
        board.o(0, 2)
        self.assertFalse(board.clone().is_free(0, 2))

    def test_clone_detaches_future_writes(self):
        board = Board()
        board2 = board.clone()
        board.o(0, 2)
        self.assertTrue(board2.is_free(0, 2))

if __name__ == '__main__':
    unittest.main()
