import string
from copy import deepcopy
from typing import List, Tuple, Optional

from exceptions import NoSuchOption


class SudokuBoard(object):
    def __init__(
            self, size: int, *,
            initiate_state: List[List[Optional[str]]] = None, option_fill: str = ' ', fill: str = ' '
    ):
        self.option_fill = option_fill
        self.fill = fill
        self.size = size
        self._table = [[None] * self.size ** 2 for _ in range(self.size ** 2)]
        self._options_table = self._generate_options_table()
        if initiate_state is not None:
            if len(initiate_state) == self.size ** 2 and all(len(i) == self.size ** 2 for i in initiate_state):
                for i, raw in enumerate(initiate_state):
                    for j, cell in enumerate(raw):
                        if cell:
                            self[i, j] = cell
            else:
                raise Exception(
                    f'{SudokuBoard.__name__} initiate_state should be the size: {self.size ** 2} × {self.size ** 2}'
                )

    def _get_all_available_options(self) -> List[str]:
        return [*(string.digits + string.ascii_uppercase)[1: self.size ** 2 + 1]]

    def _generate_options_table(self) -> List[List[List[str]]]:
        return [[self._get_all_available_options() for _ in range(self.size ** 2)] for _ in range(self.size ** 2)]

    @property
    def options_table(self) -> List[List[List[str]]]:
        return deepcopy(self._options_table)

    def calc_place(self, raw: int, column: int) -> Tuple[int, int]:
        return raw * (self.size + 1), column * (self.size + 1)

    def fill_output(self, output: List[List[str]]):
        for i, raw in enumerate(self._table):
            for j, cell in enumerate(raw):
                output_raw, output_column = self.calc_place(i, j)
                if cell:
                    offset = 1
                    output[output_raw + offset][output_column + offset] = cell
                else:
                    for k, option in enumerate(self._options_table[i][j]):
                        raw_offset = k // self.size
                        column_offset = k % self.size
                        output[output_raw + raw_offset][output_column + column_offset] = option or self.fill

    def get_cell_options(self, raw: int, column: int) -> List[str]:
        return [option for option in self._options_table[raw][column] if option != self.fill]

    def mark_option(self, raw: int, column: int, option: str):
        if option not in self._options_table[raw][column] or self._table[raw][column]:
            return
        option_index = self._options_table[raw][column].index(option)
        self._options_table[raw][column][option_index] = self.option_fill

    def __str__(self):
        output_length = (((self.size + 1) * self.size) * self.size - 1,) * 2
        output = [[self.fill] * output_length[0] for _ in range(output_length[1])]
        self.fill_output(output)
        return '\n'.join(''.join(raw) for raw in output)

    def __getitem__(self, key) -> Optional[str]:
        raw, column = key
        return self._table[raw][column]

    def __setitem__(self, key, value):
        raw, column = key
        if value not in self._options_table[raw][column]:
            raise NoSuchOption()
        for option in self._options_table[raw][column]:
            if option != value:
                self.mark_option(raw, column, option)
        self._table[raw][column] = value

    def __iter__(self):
        return self._table.__iter__()
