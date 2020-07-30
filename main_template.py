from sudoku_solver import SudokuSolver

# here you need to enter the initial state of the sudoku
SUDOKU_INITIAL_STATE = [
    ['', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', ''],

    ['', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', ''],

    ['', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', ''],
]


def main():
    s = SudokuSolver(initiate_state=SUDOKU_INITIAL_STATE)
    s.solve()
    print(s)


if __name__ == '__main__':
    main()
