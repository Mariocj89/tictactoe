from __future__ import print_function
import random
import itertools
from tictactoe import board


class HumanPlayer(object):
    """Represents a player that interacts through stdin"""

    TITLE = "Human"

    def __init__(self, in_board):
        """Initializes the player with a handle the the board where the game is played

        The player should not modify the board directly
        """
        self.board = in_board

    def play(self):
        """Returns the desired movement of the player"""
        print(self.board)
        while True:
            try:
                row = int(raw_input("row: "))
                column = int(raw_input("column: "))
            except ValueError:
                print("Invalid number")
                continue
            if not(0 <= row <= 2) or not(0 <= column <= 2):
                print("Invalid position")
                continue
            if not self.board.is_free(row, column):
                print("Position already taken")
                continue
            return row, column


class RandomComputerPlayer(object):
    """IA player that plays randomly"""

    TITLE = "Random IA"

    def __init__(self, in_board):
        self.board = in_board

    def play(self):
        """Returns the desired movement of the player"""
        while True:
            row = random.randint(0, 2)
            column = random.randint(0, 2)
            if self.board.is_free(row, column):
                break
        return row, column


class Game(object):
    """Class to handle all interaction between players and the board"""
    def __init__(self):
        self.board = board.Board()
        options = [board.CROSS, board.CIRCLE]
        random.shuffle(options)
        self.turns = itertools.cycle(options)

    def create_player(self):
        options = {
            "H": HumanPlayer,
            "R": RandomComputerPlayer,
        }
        while True:
            print("Choose a Player: ")
            for k, v in options.items():
                print("{}) {}".format(k, v.TITLE))
            option = raw_input("Type Initial: ")[0]
            if option[0] in options:
                res = options[option]
                print("You have chosen: {}".format(res.TITLE))
                return res(self.board)

    def play(self):
        cross_player = self.create_player()
        circle_player = self.create_player()
        while True:
            turn = next(self.turns)

            print("Turn of: '{}'".format(turn))
            if turn == board.CROSS:
                row, column = cross_player.play()
                self.board.x(row, column)
            elif turn == board.CIRCLE:
                row, column = circle_player.play()
                self.board.o(row, column)

            if self.board.winner:
                print("{} wins!".format(self.board.winner))
                return 0
            if self.board.completed:
                print("Game Finished")
                return 0
