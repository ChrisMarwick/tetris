import logging
import random
from abc import ABC
from math import sin, cos, radians




class TetrominoFactory:

    def __init__(self, grid):
        self.grid = grid
        self.current_bag = None

    @staticmethod
    def _create_tetromino_bag():
        """
        We generate tetrominos at random, to avoid creating multiple tetrominos of the same type in a row, we put all 
        possible tetrominos into a bag with random position and take tetrominos out of the bag until it's empty, then 
        regenerate the bag. 
        """
        bag = [TetrominoI, TetrominoJ, TetrominoL, TetrominoO, TetrominoS, TetrominoT, TetrominoZ]
        random.shuffle(bag)
        return bag


    def create_tetromino(self, start_row, start_column):
        if not self.current_bag:
            _CURRENT_BAG = self._create_tetromino_bag()
        TetrominoCls = _CURRENT_BAG.pop()
        logging.info(f'Creating tetromino {TetrominoCls}')
        return TetrominoCls(self.grid, start_row, start_column)


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
            logging.debug(f'Setting cell {(row, column)} to empty')
            self.grid.set_cell_empty(row, column)

    def _add_to_grid(self):
        positions = []
        for relative_row, relative_column in self.relative_cell_positions:
            row, column = self._relative_position_to_absolute((relative_row, relative_column))
            positions.append((row, column))
            if self.grid.is_cell_occupied(row, column):
                raise MovementBlocked
        for row, column in positions:
            logging.debug(f'Setting cell {(row, column)} to visited')
            self.grid.set_cell_visited(row, column, None)

    @classmethod
    def initial_cell_relative_positions(cls):
        raise NotImplementedError

    def _move(self, row_displacement, column_displacement):
        # Check if we can move the tetromino at all
        new_positions = [
            self._relative_position_to_absolute((row + row_displacement, column + column_displacement)) 
            for row, column in self.relative_cell_positions
        ]
        for row, column in new_positions:
            if row >= self.grid.num_rows or column < 0 or column >= self.grid.num_columns or self.grid.is_cell_occupied(row, column):
                raise MovementBlocked
            
        # Update the tetromino's position and it's cell occupancy on the grid
        self._remove_from_grid()
        self.position = (self.position[0] + row_displacement, self.position[1] + column_displacement)
        self._add_to_grid()

    def move_down(self):
        self._move(1, 0)

    def move_left(self):
        self._move(0, -1)

    def move_right(self):
        self._move(0, 1)

    def lock(self):
        for relative_position in self.relative_cell_positions:
            row, column = self._relative_position_to_absolute(relative_position)
            logging.debug(f'Setting cell {(row, column)} to occupied')
            self.grid.set_cell_occupied(row, column, None)

    def drop(self):
        max_drop = None
        for row, column in [self._relative_position_to_absolute(position) for position in self.relative_cell_positions]:
            current_cell_max_drop = 0
            while row + current_cell_max_drop + 1 < self.grid.num_rows and not self.grid.is_cell_occupied(row + current_cell_max_drop + 1, column):
                current_cell_max_drop += 1
            max_drop = min(max_drop, current_cell_max_drop) if max_drop is not None else current_cell_max_drop
        self._remove_from_grid()
        self.position = (self.position[0] + max_drop, self.position[1])
        self._add_to_grid()
        self.lock()

    def _rotate(self, degrees):
        new_relative_cell_positions = []
        for row, column in self.relative_cell_positions:
            new_row = round(column * sin(radians(degrees)) + row * cos(radians(degrees)))
            new_column = round(column * cos(radians(degrees)) - row * sin(radians(degrees)))
            new_relative_cell_positions.append((new_row, new_column))
        # Check the tetromino can be rotated without hitting the bottom of the grid/an occupied cell
        new_positions = [self._relative_position_to_absolute(position) for position in new_relative_cell_positions]
        for row, column in new_positions:
            if row >= self.grid.num_rows or self.grid.is_cell_occupied(row, column):
                raise MovementBlocked
        self._remove_from_grid()
        self.relative_cell_positions = new_relative_cell_positions
        self._add_to_grid()

    def rotate_anticlockwise(self):
        return self._rotate(-90)

    def rotate_clockwise(self):
        return self._rotate(90)
    

class TetrominoI(Tetromino):

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, -1), (0, 1), (0, 2)]
    

class TetrominoJ(Tetromino):

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (-1, 0), (0, 1), (0, 2)]
    

class TetrominoL(Tetromino):

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, -1), (-1, 1), (0, 1)]
    

class TetrominoO(Tetromino):

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, 1), (1, 1), (1, 0)]
    

class TetrominoS(Tetromino):

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, 1), (1, 0), (1, -1)]


class TetrominoT(Tetromino):

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (-1, 0), (0, -1), (0, 1)]
    

class TetrominoZ(Tetromino):

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, -1), (1, 0), (1, 1)]
