from abc import ABC
from math import sin, cos, radians


class MovementBlocked(Exception):
    pass


class Tetromino(ABC):

    def __init__(self, grid, start_row, start_column):
        self.grid = grid
        self.position = (start_row, start_column)
        self.relative_cell_positions = self.initial_cell_relative_positions()
        self._add_to_grid()
            
    def _relative_position_to_absolute(self, relative_position):
        return (self.position[0] + relative_position[0], self.position[1] + relative_position[1])
    
    def _remove_from_grid(self):
        for relative_row, relative_column in self.relative_cell_positions:
            row, column = self._relative_position_to_absolute((relative_row, relative_column))
            self.grid.set_cell_unoccupied(row, column)

    def _add_to_grid(self):
        positions = []
        for relative_row, relative_column in self.relative_cell_positions:
            row, column = self._relative_position_to_absolute((relative_row, relative_column))
            positions.append((row, column))
            if self.grid.is_cell_occupied(row, column):
                raise MovementBlocked
        for row, column in positions:
            self.grid.set_cell_occupied(row, column, None)

    @classmethod
    def initial_cell_relative_positions(cls):
        raise NotImplementedError

    def move_down(self):
        self._remove_from_grid()
        self.position = (self.position[0] + 1, self.position[1])
        self._add_to_grid()
        # TODO: handle when we hit the bottom of the grid

    def drop(self):
        self._remove_from_grid()

    def _rotate(self, degrees):
        self._remove_from_grid()
        new_relative_cell_positions = []
        for row, column in self.relative_cell_positions:
            new_row = column * sin(radians(degrees)) + row * cos(radians(degrees))
            new_column = column * cos(radians(degrees)) - row * sin(radians(degrees))
            new_relative_cell_positions.append((new_row, new_column))
        self.relative_cell_positions = new_relative_cell_positions
        self._add_to_grid()

    def rotate_left(self):
        return self._rotate(-90)

    def rotate_right(self):
        return self._rotate(90)