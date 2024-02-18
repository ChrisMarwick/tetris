from .tetromino import Tetromino


class TetrominoL(Tetromino):

    @classmethod
    def initial_cell_relative_positions(cls):
        return [(0, 0), (0, -1), (0, 1), (0, 2)]