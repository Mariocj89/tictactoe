from __future__ import print_function
import random
import itertools
from tictactoe import board

try:
    input = raw_input
except NameError:
    pass


class Player(object):

    TITLE = 'N/A'

    def __init__(self, role, in_board):
        """Initializes the player with a handle the the board where the game is played"""
        self.role = role
        self.board = in_board
        assert role in [board.CIRCLE, board.CROSS]

    @staticmethod
    def _play(role, in_board, row, column):
        """Plays a movement given all parameters"""
        if role == board.CROSS:
            in_board.x(row, column)
        else:
            in_board.o(row, column)

    def play(self):
        """Makes a movement"""
        row, column = self._next_movement()
        self._play(self.role, self.board, row, column)
        print("{} plays {}, {}".format(self, row, column))

    def _next_movement(self):
        """Returns the a tuple that represents the desired movement of the player"""
        raise NotImplementedError()

    def __str__(self):
        return "{} {}".format(self.role, self.TITLE)


class HumanPlayer(Player):
    """Represents a player that interacts through stdin"""

    TITLE = "Human"

    def _next_movement(self):
        print(self.board)
        while True:
            try:
                row = int(input("row: "))
                column = int(input("column: "))
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


class RandomComputerPlayer(Player):
    """IA player that plays randomly"""

    TITLE = "Random IA"

    def _next_movement(self):
        while True:
            row = random.randint(0, 2)
            column = random.randint(0, 2)
            if self.board.is_free(row, column):
                break
        return row, column


class GodComputerPlayer(Player):
    """IA player that plays by analysing all options"""

    TITLE = "God IA"

    WIN_WEIGHT = 2
    LOOSE_WEIGHT = -10
    TIE_WEIGHT = 0

    def _compute_score(self, in_board, row, column):
        """Gets the heuristics of a movement the higher the better"""
        res_board = in_board.clone()
        self._play(self.role, res_board, row, column)
        if res_board.winner:
            if res_board.winner == self.role:
                return self.WIN_WEIGHT
            else:
                return self.LOOSE_WEIGHT
        elif res_board.completed:
            return self.TIE_WEIGHT
        else:
            adversary_role = board.CROSS if self.role == board.CIRCLE else board.CIRCLE
            adversary = GodComputerPlayer(adversary_role, res_board)
            r, c = adversary._next_movement()
            adversary._play(adversary_role, res_board, r, c)
            movements = [x for x in itertools.product(range(3), range(3)) if res_board.is_free(*x)]
            scores = [self._compute_score(res_board, x[0], x[1]) for x in movements]
            return sum(scores)

    def _next_movement(self):
        movements = [x for x in itertools.product(range(3), range(3)) if self.board.is_free(*x)]
        scores = [(self._compute_score(self.board, x[0], x[1]), x) for x in movements]
        _, best_move = max(scores)
        return best_move


class Game(object):
    """Class to handle all interaction between players and the board"""
    def __init__(self):
        self.board = board.Board()

    def create_player(self, role):
        options = {
            "H": HumanPlayer,
            "R": RandomComputerPlayer,
            "G": GodComputerPlayer,
        }
        while True:
            print("Choose a Player for {}: ".format(role))
            for k, v in options.items():
                print("{}) {}".format(k, v.TITLE))
            option = input("Type Initial: ")[0]
            if option[0] in options:
                res = options[option]
                print("You have chosen: {}".format(res.TITLE))
                return res(role, self.board)

    def play(self):
        players = [self.create_player(board.CROSS),
                   self.create_player(board.CIRCLE)]
        random.shuffle(players)
        players = itertools.cycle(players)
        while True:
            player = next(players)

            print("Turn of: '{}'".format(player))
            player.play()

            if self.board.winner:
                print("{} wins!".format(self.board.winner))
                return 0
            if self.board.completed:
                print("Game Finished")
                return 0
