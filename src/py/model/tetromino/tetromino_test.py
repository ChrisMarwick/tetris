from grid import Grid
from .tetromino_l import TetrominoL


class TestTetromino:

    def test_rotate_left():
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 2, 2)
        assert grid.is_cell_occupied(2, 1)
        assert grid.is_cell_occupied(2, 2)
        assert grid.is_cell_occupied(2, 3)
        assert grid.is_cell_occupied(2, 4)
        # tetromino.rotate_left()