class SudokuError(RuntimeError):
    def __init__(self, msg):
        super().__init__(msg)


class NoOptionsException(SudokuError):
    def __init__(self):
        super().__init__('one of the cells has no options')


class NoSuchOption(SudokuError):
    def __init__(self):
        super().__init__('the value must be in the options')
