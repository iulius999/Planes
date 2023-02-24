import time

from exceptions import OutsideBoardError, PlaneOverlapError, AlreadyHitError
from game import Game


class UI:

    def __init__(self, game: Game):
        self._game = game
        print('\nWelcome to Planes!')
        print('For choosing the position of a plane, type the desired cell for the head of the plane. Example: C9')
        print('The direction in which a plane points can be chosen by typing Up/Down/Left/Right. Example: down')

    def start(self):
        correct_planes = 0

        while True:
            print('\nYour board:\n')
            print(self._game.human_board())

            if correct_planes == 3:
                break

            print('Position')
            row, col = self._input_position()
            if row == -1 and col == -1:
                continue

            print('Direction')
            d = self._input_direction()
            if d == -1:
                continue

            try:
                self._game.create_plane_human(row, col, d)
                correct_planes += 1
            except OutsideBoardError as obe:
                print(str(obe))
            except PlaneOverlapError as poe:
                print(str(poe))

        print('\nWho will hit first?')
        print('\t1. You')
        print('\t2. Enemy\n')

        move = 0
        while True:
            opt = input('>>> ')
            opt = opt.strip()

            if opt not in ['1', '2']:
                print('Invalid option!')
                continue

            move = int(opt)
            break

        while True:
            print()
            print(self._game.both_boards())

            winner = self._game.winner()
            if winner == 1:
                print('CONGRATULATIONS! You WON the game!')
                break
            elif winner == 2:
                print('Game over. You lost!')
                break

            if move == 1:
                print('Your time to hit')

                while True:
                    row, col = self._input_position()
                    if row == -1 and col == -1:
                        continue
                    try:
                        self._game.update_computer_board(row, col)
                        self._game.increase_score_human(row, col)
                        break
                    except AlreadyHitError as ahe:
                        print(str(ahe))

            else:
                time.sleep(2)
                print(3)
                time.sleep(1)
                print(2)
                time.sleep(1)
                print(1)
                time.sleep(1)
                print('Enemy hits...')
                time.sleep(1)

                row, col = self._game.hit_computer()
                print('Your enemy hit ' + self._game.to_cell(row, col) + '!')
                self._game.update_human_board(row, col)
                self._game.increase_score_computer(row, col)
                self._game.next_moves(row, col)

            move = 3 - move

    @staticmethod
    def _input_position():
        cell = input('>>> ')
        cell = cell.strip()

        if len(cell) != 2 and len(cell) != 3:
            print('Invalid position!')
            return -1, -1

        if cell[0].upper() not in [chr(65 + i) for i in range(10)]:
            print('Invalid position!')
            return -1, -1

        row = ord(cell[0].upper()) - 65
        col = -1

        try:
            col = int(cell[1:]) - 1
        except ValueError:
            print('Invalid position!')
            return -1, -1

        if col not in list(range(10)):
            print('Invalid position!')
            return -1, -1

        return row, col

    @staticmethod
    def _input_direction():
        d = input('>>> ')
        d = d.strip()

        directions = {'up': 0, 'down': 1, 'left': 2, 'right': 3}

        if d not in directions:
            print('Invalid direction!')
            return -1

        return directions[d]
