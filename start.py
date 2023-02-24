from src.board.board import Board
from src.game.game import Computer, Game
from src.ui.ui import UI

if __name__ == '__main__':
    human_board = Board()
    computer_board = Board()
    computer = Computer()

    planes = Game(human_board, computer_board, computer)

    ui = UI(planes)
    ui.start()
