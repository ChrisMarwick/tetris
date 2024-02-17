from .tetromino import Tetromino


class TetrominoL(Tetromino):

    @classmethod
    def cells(cls):
        return [(0, 0), (0, -1), (0, 1), (0, 2)]