import logging
from abc import ABC
from enum import Enum
from math import sin, cos, radians
from model.grid import Grid


class MovementBlocked(Exception):
    """
    Exception when we can't perform a tetromino movement/rotation due to the space it would take being occupied already
    """


class TetrominoColor(Enum):
    """Possible colors a tetromino can take"""

    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    BLUE = "BLUE"
    PURPLE = "PURPLE"

    def get_raw_color(self):
        return self.value.lower()


class Tetromino(ABC):
    """Base class for a tetromino, and all the actions that are possible to take on it"""

    def __init__(
        self, grid: Grid, start_row: int, start_column: int, color: TetrominoColor
    ):
        self.grid = grid
        self.position = (start_row, start_column)
        self.color = color
        self.relative_cell_positions = self.initial_cell_relative_positions()
        self._add_to_grid()

    def _relative_position_to_absolute(self, relative_position):
        return (
            self.position[0] + relative_position[0],
            self.position[1] + relative_position[1],
        )

    @property
    def absolute_cell_positions(self):
        return [
            self._relative_position_to_absolute(pos)
            for pos in self.relative_cell_positions
        ]

    def _remove_from_grid(self):
        for row, column in self.absolute_cell_positions:
            logging.debug("Setting cell %s to empty", (row, column))
            self.grid.set_cell_empty(row, column)

    def _add_to_grid(self):
        positions = []
        for row, column in self.absolute_cell_positions:
            positions.append((row, column))
            if self.grid.is_cell_occupied(row, column):
                raise MovementBlocked
        for row, column in positions:
            logging.debug("Setting cell %s to visited", (row, column))
            self.grid.set_cell_visited(row, column, self.color.value)

    @classmethod
    def initial_cell_relative_positions(cls):
        raise NotImplementedError

    def _move(self, row_displacement, column_displacement):
        # Check if we can move the tetromino at all
        new_positions = [
            self._relative_position_to_absolute(
                (row + row_displacement, column + column_displacement)
            )
            for row, column in self.relative_cell_positions
        ]
        for row, column in new_positions:
            if (
                row >= self.grid.num_rows
                or column < 0
                or column >= self.grid.num_columns
                or self.grid.is_cell_occupied(row, column)
            ):
                raise MovementBlocked

        # Update the tetromino's position and it's cell occupancy on the grid
        self._remove_from_grid()
        self.position = (
            self.position[0] + row_displacement,
            self.position[1] + column_displacement,
        )
        self._add_to_grid()

    def move_down(self):
        self._move(1, 0)

    def move_left(self):
        self._move(0, -1)

    def move_right(self):
        self._move(0, 1)

    def lock(self):
        for row, column in self.absolute_cell_positions:
            logging.debug("Setting cell %s to occupied", (row, column))
            self.grid.set_cell_occupied(row, column, self.color.value)

    def drop(self):
        max_drop = None
        for row, column in self.absolute_cell_positions:
            current_cell_max_drop = 0
            while (
                row + current_cell_max_drop + 1 < self.grid.num_rows
                and not self.grid.is_cell_occupied(
                    row + current_cell_max_drop + 1, column
                )
            ):
                current_cell_max_drop += 1
            max_drop = (
                min(max_drop, current_cell_max_drop)
                if max_drop is not None
                else current_cell_max_drop
            )
        self._remove_from_grid()
        self.position = (self.position[0] + max_drop, self.position[1])
        self.lock()

    def _rotate(self, degrees):
        new_relative_cell_positions = []
        for row, column in self.relative_cell_positions:
            new_row = round(
                column * sin(radians(degrees)) + row * cos(radians(degrees))
            )
            new_column = round(
                column * cos(radians(degrees)) - row * sin(radians(degrees))
            )
            new_relative_cell_positions.append((new_row, new_column))
        # Check the tetromino can be rotated without hitting the bottom of the grid/an occupied cell
        new_positions = [
            self._relative_position_to_absolute(position)
            for position in new_relative_cell_positions
        ]
        for row, column in new_positions:
            if (
                row < 0
                or row >= self.grid.num_rows
                or column < 0
                or column >= self.grid.num_columns
                or self.grid.is_cell_occupied(row, column)
            ):
                raise MovementBlocked
        self._remove_from_grid()
        self.relative_cell_positions = new_relative_cell_positions
        self._add_to_grid()

    def rotate_anticlockwise(self):
        return self._rotate(-90)

    def rotate_clockwise(self):
        return self._rotate(90)

    def __str__(self):
        return f"Tetromino class={self.__class__}, color={self.color.value}, position={self.absolute_cell_positions}"


class TetrominoI(Tetromino):
    """I tetromino"""

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, -1), (0, 1), (0, 2)]


class TetrominoJ(Tetromino):
    """J tetromino"""

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (-1, 0), (0, 1), (0, 2)]


class TetrominoL(Tetromino):
    """L tetromino"""

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, -1), (-1, 1), (0, 1)]


class TetrominoO(Tetromino):
    """O tetromino"""

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, 1), (1, 1), (1, 0)]


class TetrominoS(Tetromino):
    """S tetromino"""

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, 1), (1, 0), (1, -1)]


class TetrominoT(Tetromino):
    """T tetromino"""

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (-1, 0), (0, -1), (0, 1)]


class TetrominoZ(Tetromino):
    """Z tetromino"""

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, -1), (1, 0), (1, 1)]
