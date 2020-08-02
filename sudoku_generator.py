import random
from copy import deepcopy
from typing import Callable, List, Tuple

from exceptions import SudokuError
from sudoku_solver import SudokuSolver


class SudokuGenerator(SudokuSolver):
    def generate_random_sudoku(self, *, shuffle: Callable[[List[str]], None] = random.shuffle) -> bool:
        if self.try_solve():
            return True
        for i, row in enumerate(self.sudoku_board):
            for j, cell in enumerate(row):
                if cell:
                    continue
                cell_options = self.sudoku_board.get_cell_options(i, j)
                shuffle(cell_options)
                for option in cell_options:
                    temp_solver = deepcopy(self)
                    temp_solver.sudoku_board[i, j] = option
                    try:
                        if temp_solver.generate_random_sudoku(shuffle=shuffle):
                            self.sudoku_board = temp_solver.sudoku_board
                            return True
                    except SudokuError:
                        pass
                return False
        return False

    def remove_value_if_possible(self, key: Tuple[int, int]) -> bool:
        value = self.sudoku_board[key]
        self.sudoku_board[key] = None
        temp_solver = SudokuSolver(self.sudoku_board.size, initiate_state=[*self.sudoku_board])
        solutions = temp_solver.get_solutions()
        next(solutions)
        try:
            next(solutions)
            self.sudoku_board[key] = value
            return False
        except StopIteration:
            return True

    def generate_random_minimal_sudoku(self, *, shuffle: Callable[[List], None] = random.shuffle) -> bool:
        if not self.generate_random_sudoku(shuffle=shuffle):
            return False
        keys = [(i, j) for i in range(self.sudoku_board.size ** 2) for j in range(self.sudoku_board.size ** 2)]
        shuffle(keys)
        for key in keys:
            self.remove_value_if_possible(key)
        return True
