from __future__ import annotations
from typing import Iterable, Sequence
import numpy as np

class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        puzzle_new = np.ndarray(shape=(9,9), dtype=int)
        count = 0
        for line in puzzle:

            line =  [int(i) for i in line ]
            puzzle_new[count,:] = line
            count += 1

        self._grid = puzzle_new

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y,x] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""

        self._grid[y,x] = 0


    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        value = self._grid[y,x]

        return value

    def options_at(self, x: int, y: int) -> Sequence[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # Remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        zero_indices = np.where(self._grid==0)


        if len(self._grid[zero_indices]) == 0:
            return next_x, next_y
        else:
            next_x =zero_indices[1][0]
            next_y = zero_indices[0][0]


        return next_x, next_y

    def row_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th row."""
        values = self._grid[i,:]

        return values

    def column_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th column."""
        values = self._grid[:,i]

        return values

    def block_values(self, i: int) -> Sequence[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []
        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        mini_grid = self._grid[y_start:y_start+3 ,  x_start:x_start+3  ]

        for i in np.nditer(mini_grid):
            values.append(i.tolist())

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        result = True

        for i in range(9):
            for value in values:
                if value not in self.column_values(i):
                    return False

                if value not in self.row_values(i):
                    return False

                if value not in self.block_values(i):
                    return False

        return result

    def __str__(self) -> str:

        representation = np.array2string( self._grid)

        return representation


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle = []
    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip()
            line = line.split(',')

            puzzle.append(line)

    return Sudoku(puzzle)

