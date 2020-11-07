from math import sqrt, pow
from copy import deepcopy


class SudokuBase:
    def __init__(self, question):
        self.verbose = False
        self._question = question
        self._size = len(self._question)
        self._unit = int(sqrt(self._size))
        self._digit = len(str(self._size))

    def get_size(self) -> int:
        return self._size

    def get_question(self) -> list:
        return deepcopy(self._question)

    def _check_unique(self) -> bool:
        is_unique = True
        # row check
        for r in range(self._size):
            counter = [0 for i in range(self._size)]
            for c in range(self._size):
                if self._question[r][c] != 0:
                    counter[self._question[r][c]-1] += 1
                    if counter[self._question[r][c]-1]>1:
                        if self.verbose:
                            print('row check violation')
                        is_unique = False
        # col check
        for c in range(self._size):
            counter = [0 for i in range(self._size)]
            for r in range(self._size):
                if self._question[r][c] != 0:
                    counter[self._question[r][c]-1] += 1
                    if counter[self._question[r][c]-1] > 1:
                        if self.verbose:
                            print('col check violation')
                        is_unique = False
        # matrix check
        for r in range(self._unit):
            for c in range(self._unit):
                counter = [0 for i in range(self._size)]
                for r2 in range(self._unit):
                    for c2 in range(self._unit):
                        if self._question[r*self._unit+r2][c*self._unit+c2]!=0:
                            counter[self._question[r*self._unit+r2][c*self._unit+c2] - 1] += 1
                            if counter[self._question[r*self._unit+r2][c*self._unit+c2] - 1] > 1:
                                if self.verbose:
                                    print('matrix check violation')
                                is_unique = False
        if self.verbose and is_unique:
            print('no problem')

        return is_unique

    def print_question(self) -> None:
        for r in range(self._size):
            if r % self._unit == 0 and r != 0:
                for i in range((self._digit + 1) * self._size - 1):
                    if i % ((self._digit + 1) * self._unit) == ((self._digit + 1) * self._unit - 1) and i != (
                            self._digit + 1) * self._size - 2:
                        print('+', end='')
                    else:
                        print('-', end='')
                print('')
            for c in range(self._size):
                display_string = self._question[r][c] if self._question[r][c] != 0 else " "
                display_string = str(display_string).rjust(self._digit, " ")
                if c % self._unit == self._unit - 1 and c != self._size - 1 and c != 0:
                    display_string += '|'
                elif c == self._size - 1:
                    pass
                else:
                    display_string += ','
                print(display_string, end='')
            print('')


class SudokuCheckQuestion(SudokuBase):
    def __init__(self, question):
        super().__init__(question)
        self._valid_question = self._check_valid_question()

    def get_valid(self) -> bool:
        return self._valid_question

    def _check_valid_question(self) -> bool:
        is_valid_question = True
        if pow(self._unit, 2) != self._size:
            if self.verbose:
                print('square num check false')
            is_valid_question = False

        for i in range(self._size):
            if len(self._question[i]) != self._size:
                if self.verbose:
                    print('length consistency check false')
                is_valid_question = False
        if not self._check_unique():
            if self.verbose:
                print('duplicate check false')
            is_valid_question = False

        return is_valid_question


class Sudoku(SudokuBase):
    def __init__(self, question):
        super().__init__(question)
        self._next_position = self._search_max_constraint()
        self._next_r = self._next_position['r']
        self._next_c = self._next_position['c']
        self._next_value = 0

    def set_next_value(self, i):
        self._next_value = i

    def set_next_value_to_question(self):
        self._question[self._next_r][self._next_c] = self._next_value

    def _output_square_range(self, i):
        sqrt_idx = i // self._unit
        idx_min = sqrt_idx * self._unit
        idx_max = (sqrt_idx + 1) * self._unit
        return {'idx_min': idx_min, 'idx_max': idx_max}

    def _search_max_constraint(self):
        strength_constraint = [[0 for i in range(self._size)] for j in range(self._size)]
        for r in range(self._size):
            for c in range(self._size):
                if self._question[r][c] == 0:
                    counter = [0 for i in range(self._size)]
                    strength = 0
                    # matrix check
                    r_idx = self._output_square_range(r)
                    c_idx = self._output_square_range(c)
                    for x in range(r_idx['idx_min'], r_idx['idx_max']):
                        for y in range(c_idx['idx_min'], c_idx['idx_max']):
                            if self._question[x][y] != 0:
                                counter[self._question[x][y] - 1] = 1
                    # row check
                    for y in range(self._size):
                        if self._question[r][y] != 0:
                            counter[self._question[r][y] - 1] = 1
                    # col check
                    for x in range(self._size):
                        if self._question[x][c] != 0:
                            counter[self._question[x][c] - 1] = 1
                    for count in counter:
                        strength += count
                    strength_constraint[r][c] = strength
        strength_max = -1
        position = {}
        for r in range(self._size):
            for c in range(self._size):
                if strength_constraint[r][c] > strength_max:
                    strength_max = strength_constraint[r][c]
                    position['r'] = r
                    position['c'] = c
        return position

    def check_insert(self):
        able_insert = True

        # row check
        for c in range(self._size):
            if self._question[self._next_r][c] == self._next_value:
                if self.verbose:
                    print('row check violation')
                able_insert = False
        # col check
        for r in range(self._size):
            if self._question[r][self._next_c] == self._next_value:
                if self.verbose:
                    print('col check violation')
                able_insert = False
        # matrix check
        r_idx = self._output_square_range(self._next_r)
        c_idx = self._output_square_range(self._next_c)
        for x in range(r_idx['idx_min'], r_idx['idx_max']):
            for y in range(c_idx['idx_min'], c_idx['idx_max']):
                if self._question[x][y] == self._next_value:
                    if self.verbose:
                        print('matrix check violation')
                    able_insert = False
        return able_insert

    def check_complete(self):
        is_completed = True
        if self._check_unique():
            for r in range(self._size):
                for c in range(self._size):
                    if self._question[r][c] == 0:
                        is_completed = False
        else:
            is_completed = False
        return is_completed
