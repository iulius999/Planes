import texttable


class Board:

    def __init__(self):
        self._data = [['.' for j in range(10)] for i in range(10)]
        self._visible = [[False for j in range(10)] for i in range(10)]
        # ' ' - air
        # '#' - hit
        # 'x' - dead
        # '*' - part of a plane
        # '^', 'v', '>', '<' - head of a plane
        # '.' - not visible yet

    def get_symbol(self, row, col: int):
        return self._data[row][col]

    def set_symbol(self, row, col: int, symbol):
        self._data[row][col] = symbol

    def make_visible(self, row, col):
        self._visible[row][col] = True

    @staticmethod
    def on_board(row, col: int) -> bool:
        if 0 <= row < 10 and 0 <= col < 10:
            return True
        return False

    def __str__(self):
        board = '\t  1 2 3 4 5 6 7 8 9 10\n'

        for i in range(10):
            board += '\t' + chr(65 + i) + ' '
            for j in range(10):
                if self._visible[i][j]:
                    board += self.get_symbol(i, j) + ' '
                else:
                    board += '.' + ' '
            board += '\n'

        return board

    # def __str__(self):
    #     t = texttable.Texttable()
    #
    #     t.add_row([' '] + list(range(1, 11)))
    #
    #     for i in range(10):
    #         curr_row = [chr(65 + i)]
    #         for j in range(10):
    #             if self._visible[i][j]:
    #                 curr_row.append(self.get_symbol(i, j))
    #             else:
    #                 curr_row.append('.')
    #
    #         t.add_row(curr_row)
    #
    #     return t.draw()


# if __name__ == '__main__':
#     b = Board()
#     print(b)
