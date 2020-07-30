from typing import List, Optional

from sudoku_board import SudokuBoard

BASIC_SIZE = 3


class SudokuSolver(object):
    def __init__(
            self, board_size: int = BASIC_SIZE, *,
            initiate_state: List[List[Optional[str]]] = None, option_fill: str = ' ', fill: str = ' '
    ):
        self.sudoku_board = SudokuBoard(board_size, initiate_state=initiate_state, option_fill=option_fill, fill=fill)

    def _fill_only_option(self):
        for i, options_raw in enumerate(self.sudoku_board.options_table):
            for j in range(len(options_raw)):
                if self.sudoku_board[i, j]:
                    continue
                cell_options = self.sudoku_board.get_cell_options(i, j)
                if cell_options == 1:
                    self.sudoku_board[i, j] = cell_options[0]

    def _get_only_options_indexes(self, options_indexes):
        only_option_indexes = {}
        for options_index in options_indexes:
            cell_options = self.sudoku_board.get_cell_options(*options_index)
            for option in cell_options:
                if option in only_option_indexes:
                    only_option_indexes[option] = None
                else:
                    only_option_indexes[option] = options_index
        return {key: value for key, value in only_option_indexes.items() if value and not self.sudoku_board[value]}

    def _fill_block_options(self):
        for raw in range(0, self.sudoku_board.size ** 2, self.sudoku_board.size):
            for column in range(0, self.sudoku_board.size ** 2, self.sudoku_board.size):
                options_indexes = [
                    (raw + i, column + j)
                    for i in range(self.sudoku_board.size) for j in range(self.sudoku_board.size)
                ]
                for option, option_index in self._get_only_options_indexes(options_indexes).items():
                    self.sudoku_board[option_index] = option

    def _fill_column_options(self):
        for j in range(self.sudoku_board.size ** 2):
            options_indexes = [(i, j) for i in range(self.sudoku_board.size ** 2)]
            for option, option_index in self._get_only_options_indexes(options_indexes).items():
                self.sudoku_board[option_index] = option

    def _fill_raw_options(self):
        for i in range(self.sudoku_board.size ** 2):
            options_indexes = [(i, j) for j in range(self.sudoku_board.size ** 2)]
            for option, option_index in self._get_only_options_indexes(options_indexes).items():
                self.sudoku_board[option_index] = option

    def fill_solved_options(self):
        self._fill_only_option()
        self._fill_block_options()
        self._fill_raw_options()
        self._fill_column_options()

    def _mark_cell_relatives(self, raw, column, value):
        for i in range(self.sudoku_board.size ** 2):
            if i != raw:
                self.sudoku_board.mark_option(i, column, value)
        for j in range(self.sudoku_board.size ** 2):
            if j != column:
                self.sudoku_board.mark_option(raw, j, value)
        block_raw = raw - raw % self.sudoku_board.size
        block_column = column - column % self.sudoku_board.size
        for i in range(self.sudoku_board.size):
            for j in range(self.sudoku_board.size):
                options_raw = block_raw + i
                options_column = block_column + j
                if not (options_raw, options_column) == (raw, column):
                    self.sudoku_board.mark_option(options_raw, options_column, value)

    def mark_bad_options(self):
        for cell_raw, raw in enumerate(self.sudoku_board):
            for cell_column, cell in enumerate(raw):
                if not cell:
                    continue
                self._mark_cell_relatives(cell_raw, cell_column, cell)
