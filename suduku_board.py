from copy import deepcopy
from typing import List, Tuple

BASIC_SIZE = 3


class SudukuBoard(object):
    def __init__(self, size: int = BASIC_SIZE, *, initiate_state: List[List[str]] = None, fill: str = ' '):
        self.fill = fill
        self.size = size
        self.table = [[None] * self.size ** 2 for _ in range(self.size ** 2)]
        if initiate_state is not None:
            if len(initiate_state) == self.size ** 2 and all(len(i) == self.size ** 2 for i in initiate_state):
                self.table = deepcopy(initiate_state)
            else:
                raise Exception(
                    f'{SudukuBoard.__name__} initiate_state should be the size: {self.size ** 2} × {self.size ** 2}'
                )
        self.options_table = [[
            [str(i + 1) for i in range(self.size ** 2)] for _ in range(self.size ** 2)
        ] for _ in range(self.size ** 2)]

    def calc_place(self, raw: int, column: int) -> Tuple[int, int]:
        return raw * (self.size + 1), column * (self.size + 1)

    def fill_output(self, output: List[List[str]]):
        for i, raw in enumerate(self.table):
            for j, cell in enumerate(raw):
                output_raw, output_column = self.calc_place(i, j)
                if cell:
                    offset = 1
                    output[output_raw + offset][output_column + offset] = cell
                else:
                    for k, option in enumerate(self.options_table[i][j]):
                        raw_offset = k // self.size
                        column_offset = k % self.size
                        output[output_raw + raw_offset][output_column + column_offset] = option or self.fill

    def __str__(self):
        output_length = (((self.size + 1) * self.size) * self.size - 1,) * 2
        output = [[self.fill] * output_length[0] for _ in range(output_length[1])]
        self.fill_output(output)
        return '\n'.join(''.join(raw) for raw in output)
