from abc import ABC


class MovementBlocked(Exception):
    pass


class Tetromino(ABC):

    def __init__(self, grid, start_row, start_column):
        self.grid = grid
        self.position = (start_row, start_column)
        self.cell_positions = []
        for row_disp, column_disp in self.cells():
            row = start_row + row_disp
            column = start_column + column_disp
            self.cell_positions.append((row, column))
            if grid.is_cell_occupied(row, column, None):
                raise MovementBlocked

    @classmethod
    def cells(cls):
        raise NotImplementedError

    def move_down(self):
        for row, column in self.cell_positions:
            if self.grid.is_cell_occupied(row + 1, column):
                raise MovementBlocked
        new_cell_positions = []
        for row, column in self.cell_positions:
            self.grid.set_cell_unoccupied(row, column)
            self.grid.set_cell_occupied(row + 1, column, None)
            new_cell_positions.append((row + 1, column))
        self.cell_positions = new_cell_positions
        self.position = (self.position[0] + 1, self.position[1])

    def drop(self):
        pass

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass