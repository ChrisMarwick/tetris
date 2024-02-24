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
        # The tetramino cannot collide with itself, to avoid messiness of this sort since to check for collision we 
        # merely check if the grid cell is occupied or not we first remove the tetramino from the grid. We'll just 
        # add it back at the same position if the movement was blocked. 
        self._remove_from_grid()
        # Check if we can move the tetromino down at all
        new_positions = [self._relative_position_to_absolute((row + 1, column)) for row, column in self.relative_cell_positions]
        for row, column in new_positions:
            if row >= self.grid.num_rows or self.grid.is_cell_occupied(row, column):
                self._add_to_grid()
                raise MovementBlocked
        # Update the tetromino's position and it's cell occupancy on the grid
        self.position = (self.position[0] + 1, self.position[1])
        self._add_to_grid()

    def drop(self):
        self._remove_from_grid()
        max_drop = None
        for row, column in [self._relative_position_to_absolute(position) for position in self.relative_cell_positions]:
            current_cell_max_drop = 0
            while row + current_cell_max_drop + 1 < self.grid.num_rows and not self.grid.is_cell_occupied(row + current_cell_max_drop + 1, column):
                current_cell_max_drop += 1
            max_drop = min(max_drop, current_cell_max_drop) if max_drop is not None else current_cell_max_drop
        self.position = (self.position[0] + max_drop, self.position[1])
        self._add_to_grid()

    def _rotate(self, degrees):
        # The tetramino cannot collide with itself, to avoid messiness of this sort since to check for collision we 
        # merely check if the grid cell is occupied or not we first remove the tetramino from the grid. We'll just 
        # add it back at the same position if the rotation was blocked. 
        self._remove_from_grid()
        new_relative_cell_positions = []
        for row, column in self.relative_cell_positions:
            new_row = round(column * sin(radians(degrees)) + row * cos(radians(degrees)))
            new_column = round(column * cos(radians(degrees)) - row * sin(radians(degrees)))
            new_relative_cell_positions.append((new_row, new_column))
        # Check the tetromino can be rotated without hitting the bottom of the grid/an occupied cell
        new_positions = [self._relative_position_to_absolute(position) for position in new_relative_cell_positions]
        for row, column in new_positions:
            if row >= self.grid.num_rows or self.grid.is_cell_occupied(row, column):
                self._add_to_grid()
                raise MovementBlocked
        self.relative_cell_positions = new_relative_cell_positions
        self._add_to_grid()

    def rotate_anticlockwise(self):
        return self._rotate(-90)

    def rotate_clockwise(self):
        return self._rotate(90)