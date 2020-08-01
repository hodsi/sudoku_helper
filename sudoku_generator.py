import random
from copy import deepcopy
from typing import Callable, List

from exceptions import SudokuError
from sudoku_solver import SudokuSolver


class SudokuGenerator(SudokuSolver):
    def generate_random_sudoku(self, *, shuffle: Callable[[List[str]], None] = random.shuffle) -> bool:
        if self.try_solve():
            return True
        for i, raw in enumerate(self.sudoku_board):
            for j, cell in enumerate(raw):
                if cell:
                    continue
                cell_options = self.sudoku_board.get_cell_options(i, j)
                shuffle(cell_options)
                for option in cell_options:
                    temp_solver = deepcopy(self)
                    temp_solver.sudoku_board[i, j] = option
                    try:
                        if temp_solver.generate_random_sudoku(shuffle):
                            self.sudoku_board = temp_solver.sudoku_board
                            return True
                    except SudokuError:
                        pass
        return False
