import pytest
from model.grid import Grid
from .tetromino import MovementBlocked, TetrominoL


class TestTetromino:

    def test_move_down(self):
        grid = Grid(3, 5)
        tetromino = TetrominoL(grid, 0, 2)
        tetromino.move_down()
        assert not grid.is_cell_visited(0, 1)
        assert not grid.is_cell_visited(0, 2)
        assert not grid.is_cell_visited(0, 3)
        assert not grid.is_cell_visited(0, 4)
        assert grid.is_cell_visited(1, 1)
        assert grid.is_cell_visited(1, 2)
        assert grid.is_cell_visited(1, 3)
        assert grid.is_cell_visited(1, 4)

    def test_move_down_blocked(self):
        """We should raise a Movement Blocked exception if a move down would collide with an occupied tile"""
        grid = Grid(3, 5)
        tetromino = TetrominoL(grid, 0, 2)
        grid.set_cell_occupied(1, 4, None)
        with pytest.raises(MovementBlocked):
            tetromino.move_down()
        assert grid.is_cell_visited(0, 1)
        assert grid.is_cell_visited(0, 2)
        assert grid.is_cell_visited(0, 3)
        assert grid.is_cell_visited(0, 4)
        assert not grid.is_cell_visited(1, 1)
        assert not grid.is_cell_visited(1, 2)
        assert not grid.is_cell_visited(1, 3)
        assert grid.is_cell_occupied(1, 4)

    def test_move_down_blocked_bottom(self):
        """We should raise a Movement Blocked exception if a move down would collide with the bottom of the grid"""
        grid = Grid(3, 5)
        tetromino = TetrominoL(grid, 0, 2)
        tetromino.move_down()
        tetromino.move_down()
        with pytest.raises(MovementBlocked):
            tetromino.move_down()
        assert grid.is_cell_visited(2, 1)
        assert grid.is_cell_visited(2, 2)
        assert grid.is_cell_visited(2, 3)
        assert grid.is_cell_visited(2, 4)

    def test_rotate_anticlockwise(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 2, 2)
        tetromino.rotate_anticlockwise()
        assert grid.is_cell_visited(0, 2)
        assert grid.is_cell_visited(1, 2)
        assert grid.is_cell_visited(2, 2)
        assert grid.is_cell_visited(3, 2)
        assert not grid.is_cell_visited(2, 1)
        assert not grid.is_cell_visited(2, 3)
        assert not grid.is_cell_visited(2, 4)

    def test_rotate_blocked(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 2, 2)
        grid.set_cell_occupied(3, 2, None)
        with pytest.raises(MovementBlocked):
            tetromino.rotate_anticlockwise()
        assert grid.is_cell_visited(2, 1)
        assert grid.is_cell_visited(2, 2)
        assert grid.is_cell_visited(2, 3)
        assert grid.is_cell_visited(2, 4)
        assert not grid.is_cell_visited(0, 2)
        assert not grid.is_cell_visited(1, 2)
        assert grid.is_cell_occupied(3, 2)

    def test_rotate_blocked_bottom(self):
        grid = Grid(4, 5)
        tetromino = TetrominoL(grid, 2, 2)
        with pytest.raises(MovementBlocked):
            tetromino.rotate_clockwise()
        assert grid.is_cell_visited(2, 1)
        assert grid.is_cell_visited(2, 2)
        assert grid.is_cell_visited(2, 3)
        assert grid.is_cell_visited(2, 4)
        assert not grid.is_cell_visited(0, 2)
        assert not grid.is_cell_visited(1, 2)
        assert not grid.is_cell_visited(3, 2)

    def test_rotate_clockwise(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 2, 2)
        tetromino.rotate_clockwise()
        assert grid.is_cell_visited(1, 2)
        assert grid.is_cell_visited(2, 2)
        assert grid.is_cell_visited(3, 2)
        assert grid.is_cell_visited(4, 2)
        assert not grid.is_cell_visited(2, 1)
        assert not grid.is_cell_visited(2, 3)
        assert not grid.is_cell_visited(2, 4)

    def test_drop_blocked_1(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 0, 2)
        grid.set_cell_occupied(4, 1, None)
        tetromino.drop()
        assert grid.is_cell_visited(3, 1)
        assert grid.is_cell_visited(3, 2)
        assert grid.is_cell_visited(3, 3)
        assert grid.is_cell_visited(3, 4)
        assert not grid.is_cell_visited(0, 1)
        assert not grid.is_cell_visited(0, 2)
        assert not grid.is_cell_visited(0, 3)
        assert not grid.is_cell_visited(0, 4)
    
    def test_drop_blocked_2(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 0, 2)
        grid.set_cell_occupied(1, 2, None)
        tetromino.drop()
        assert grid.is_cell_visited(0, 1)
        assert grid.is_cell_visited(0, 2)
        assert grid.is_cell_visited(0, 3)
        assert grid.is_cell_visited(0, 4)
    
    def test_drop_blocked_bottom(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 0, 2)
        tetromino.drop()
        assert grid.is_cell_visited(4, 1)
        assert grid.is_cell_visited(4, 2)
        assert grid.is_cell_visited(4, 3)
        assert grid.is_cell_visited(4, 4)
        assert not grid.is_cell_visited(0, 1)
        assert not grid.is_cell_visited(0, 2)
        assert not grid.is_cell_visited(0, 3)
        assert not grid.is_cell_visited(0, 4)