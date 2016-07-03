import itertools

CROSS = "X"
CIRCLE = "O"
EMPTY = " "


class AlreadySet(Exception):
    """The position is already set and cannot be overridden"""
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __str__(self):
        return "Position {}, {} already set".format(self.row, self.column)


class Board(object):
    """Represents a board status"""

    def __init__(self, status=None):
        self.status = status or [[EMPTY for _ in range(3)] for _ in range(3)]

    def __str__(self):
        rows = ["|".join(row) for row in self.status]
        return "\n- - -\n".join(rows)

    @property
    def completed(self):
        return not any(any([x == EMPTY for x in row]) for row in self.status)

    def _has_won(self, player):
        combinations = [[(x, y) for x in range(3)] for y in range(3)]
        combinations += [[(y, x) for x in range(3)] for y in range(3)]
        combinations += [zip(range(3), range(3))]
        combinations += [zip(range(3), list(range(3))[::-1])]
        return any(all(self.status[x][y] == player for x, y in comb) for comb in combinations)

    def o(self, row, column):
        if self.status[row][column] != EMPTY:
            raise AlreadySet(row, column)
        self.status[row][column] = CIRCLE

    def x(self, row, column):
        if self.status[row][column] != EMPTY:
            raise AlreadySet(row, column)
        self.status[row][column] = CROSS

    @property
    def winner(self):
        """Return the player that won or None"""
        if self._has_won(CIRCLE):
            return CIRCLE
        elif self._has_won(CROSS):
            return CROSS
        else:
            return None


def main():
    import random
    board = Board()
    options = [CROSS, CIRCLE]
    random.shuffle(options)
    turns = itertools.cycle(options)
    while True:
        turn = next(turns)

        print("Turn of: '{}'".format(turn))
        while True:
            try:
                row = int(input("row: "))
                column = int(input("column: "))
            except (ValueError, NameError, SyntaxError):
                print("Invalid number")
                continue
            if not(0 <= row <= 2) or not(0 <= column <= 2):
                print("Invalid position")
                continue

            try:
                if turn == CROSS:
                    board.x(row, column)
                elif turn == CIRCLE:
                    board.o(row, column)
                break
            except AlreadySet:
                print("Position already taken")
                continue

        print(board)

        if board.winner:
            print("{} wins!".format(board.winner))
            return 0
        if board.completed:
            print("Game Finished")
            return 0


if __name__ == '__main__':
    exit(main())