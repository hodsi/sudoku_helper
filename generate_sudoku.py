import sys

from sudoku_generator import SudokuGenerator
from sudoku_solver import BASIC_SIZE


def main():
    if len(sys.argv) == 2:
        board_size = sys.argv[1]
    else:
        board_size = BASIC_SIZE
    sudoku_generator = SudokuGenerator(board_size)
    sudoku_generator.generate_random_minimal_sudoku()
    print(sudoku_generator)


if __name__ == '__main__':
    main()
