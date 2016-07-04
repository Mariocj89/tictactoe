import copy

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

    def clone(self):
        """Creates a clone of itself"""
        return Board(copy.deepcopy(self.status))

    def __init__(self, status=None):
        self.status = status or [[EMPTY for _ in range(3)] for _ in range(3)]

    def __str__(self):
        rows = ["|".join(row) for row in self.status]
        return "\n- - -\n".join(rows)

    @property
    def completed(self):
        """Wether the board is complete and no more moves can be performed"""
        return not any(any([x == EMPTY for x in row]) for row in self.status)

    def _has_won(self, player):
        """Checks if a specific player has won"""
        combinations = [[(x, y) for x in range(3)] for y in range(3)]
        combinations += [[(y, x) for x in range(3)] for y in range(3)]
        combinations += [zip(range(3), range(3))]
        combinations += [zip(range(3), list(range(3))[::-1])]
        return any(all(self.status[x][y] == player for x, y in comb) for comb in combinations)

    def o(self, row, column):
        """Places a Circle in a position"""
        if self.status[row][column] != EMPTY:
            raise AlreadySet(row, column)
        self.status[row][column] = CIRCLE

    def x(self, row, column):
        """Places a Cross in a position"""
        if self.status[row][column] != EMPTY:
            raise AlreadySet(row, column)
        self.status[row][column] = CROSS

    def is_free(self, row, column):
        """Checks if a position is free"""
        return self.status[row][column] == EMPTY

    @property
    def winner(self):
        """Return the player that won or None"""
        if self._has_won(CIRCLE):
            return CIRCLE
        elif self._has_won(CROSS):
            return CROSS
        else:
            return None

