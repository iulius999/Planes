import random

from src.board.board import Board
from src.exceptions.exceptions import OutsideBoardError, PlaneOverlapError, AlreadyHitError


class Computer:

    def __init__(self):
        self._stack = []
        self._positions = []
        self._board = [[0 for j in range(10)] for i in range(10)]
        self._expected_chance()

    def _push(self, row, col, chance):
        self._stack.append((row, col, chance))
        self._positions.remove((row, col, chance))

    def pop(self):
        if self._is_empty():
            row, col, chance = self._random_position()
            self._push(row, col, chance)

        row, col, chance = self._stack.pop()
        return row, col

    def _is_empty(self) -> bool:
        if len(self._stack) == 0:
            return True
        return False

    def adjacent_positions(self, row, col):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(directions)

        for d in range(4):
            new_row = row + directions[d][0]
            new_col = col + directions[d][1]

            if 0 <= new_row < 10 and 0 <= new_col < 10:
                new_chance = self._board[new_row][new_col]
                if self._available(new_row, new_col, new_chance):
                    self._push(new_row, new_col, new_chance)

    def _available(self, row, col, chance) -> bool:
        if (row, col, chance) in self._positions:
            return True
        return False

    @staticmethod
    def random_plane():
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        d = random.randint(0, 3)
        return row, col, d

    def _random_position(self):
        index = len(self._positions)
        for i in range(len(self._positions)):
            if self._positions[i][2] != self._positions[0][2]:
                index = i
                break

        row, col, chance = random.choice(self._positions[0:index])
        return row, col, chance

    def _expected_chance(self):
        offset = list()
        offset.append([(1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, 0), (3, -1), (3, 0), (3, 1)])  # Up
        offset.append([(-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-2, 0), (-3, -1), (-3, 0), (-3, 1)])  # Down
        offset.append([(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (0, 2), (-1, 3), (0, 3), (1, 3)])  # Left
        offset.append([(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (0, -2), (-1, -3), (0, -3), (1, -3)])  # Right

        for i in range(10):
            for j in range(10):
                for d in range(4):
                    positions = [(i, j)]
                    for off in offset[d]:
                        new_row = i + off[0]
                        new_col = j + off[1]
                        positions.append((new_row, new_col))

                    if self._check_plane_on_board(positions):
                        for cell in positions:
                            self._board[cell[0]][cell[1]] += 1

        chances = []
        for i in range(10):
            for j in range(10):
                chances.append((self._board[i][j], i, j))

        chances.sort(reverse=True)
        for ch in chances:
            self._positions.append((ch[1], ch[2], ch[0]))

    @staticmethod
    def _check_plane_on_board(positions) -> bool:
        for cell in positions:
            row = cell[0]
            col = cell[1]
            if not (0 <= row < 10 and 0 <= col < 10):
                return False
        return True


class Game:

    def __init__(self, human_board: Board, computer_board: Board, computer: Computer):
        self._human_board = human_board
        self._computer_board = computer_board
        self._computer = computer

        for row in range(10):
            for col in range(10):
                self._human_board.make_visible(row, col)

        self._create_planes_computer()

        self._score_human = 0
        self._score_computer = 0

    @staticmethod
    def _create_plane(row, col, d, board: Board):
        offset = list()
        offset.append([(1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, 0), (3, -1), (3, 0), (3, 1)])  # Up
        offset.append([(-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-2, 0), (-3, -1), (-3, 0), (-3, 1)])  # Down
        offset.append([(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (0, 2), (-1, 3), (0, 3), (1, 3)])  # Left
        offset.append([(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (0, -2), (-1, -3), (0, -3), (1, -3)])  # Right
        symbol = ['^', 'v', '<', '>']

        positions = [(row, col)]
        for off in offset[d]:
            positions.append((row + off[0], col + off[1]))

        for cell in positions:
            if not board.on_board(cell[0], cell[1]):
                raise OutsideBoardError('Plane outside board!')

        for cell in positions:
            if board.get_symbol(cell[0], cell[1]) != '.':
                raise PlaneOverlapError('Plane overlaps another plane!')

        for cell in positions:
            board.set_symbol(cell[0], cell[1], '*')

        head = positions[0]
        board.set_symbol(head[0], head[1], symbol[d])

    def create_plane_human(self, row, col, d):
        self._create_plane(row, col, d, self._human_board)

    def _create_planes_computer(self):
        correct_planes = 0

        while correct_planes < 3:
            row, col, d = self._computer.random_plane()
            try:
                self._create_plane(row, col, d, self._computer_board)
                correct_planes += 1
            except OutsideBoardError:
                pass
            except PlaneOverlapError:
                pass

    def update_computer_board(self, row, col):
        if self._computer_board.get_symbol(row, col) in [' ', '#', 'x']:
            raise AlreadyHitError('Position already hit!')

        self._computer_board.make_visible(row, col)
        symbol = self._computer_board.get_symbol(row, col)

        symbols = {'.': ' ', '*': '#', '^': 'x', 'v': 'x', '>': 'x', '<': 'x'}
        self._computer_board.set_symbol(row, col, symbols[symbol])

    def hit_computer(self):
        return self._computer.pop()

    def update_human_board(self, row, col):
        symbol = self._human_board.get_symbol(row, col)
        symbols = {'.': ' ', '*': '#', '^': 'x', 'v': 'x', '>': 'x', '<': 'x'}
        self._human_board.set_symbol(row, col, symbols[symbol])

    def next_moves(self, row, col):
        if self._human_board.get_symbol(row, col) == '#':
            self._computer.adjacent_positions(row, col)

    def increase_score_human(self, row, col):
        if self._computer_board.get_symbol(row, col) == 'x':
            self._score_human += 1

    def increase_score_computer(self, row, col):
        if self._human_board.get_symbol(row, col) == 'x':
            self._score_computer += 1

    def winner(self):
        if self._score_human == 3:
            return 1
        elif self._score_computer == 3:
            return 2
        return 0

    def human_board(self):
        return str(self._human_board)

    def both_boards(self):
        str1 = 'Your board:\n\n' + str(self._human_board)
        str2 = 'Enemy board:\n\n' + str(self._computer_board)

        split_lines = str1.split('\n')
        str1 = ''
        for line in split_lines:
            line = line.center(30, ' ')
            str1 += line + '\n'

        split_lines = str2.split('\n')
        str2 = ''
        for line in split_lines:
            line = line.center(50, ' ')
            str2 += line + '\n'

        split_lines = zip(str1.split('\n'), str2.split('\n'))
        res = '\n'.join(x + y for x, y in split_lines)

        return res

    @staticmethod
    def to_cell(row, col):
        col += 1
        row = chr(65 + row)

        return str(row) + str(col)
