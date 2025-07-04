import pytest
from model.grid import Grid
from .tetromino import (
    MovementBlocked,
    TetrominoL,
    TetrominoO,
    TetrominoI,
    TetrominoColor,
)


class TestTetromino:

    def test_move_down(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        tetromino.move_down()
        assert not grid.is_cell_visited(1, 1)
        assert not grid.is_cell_visited(1, 2)
        assert not grid.is_cell_visited(0, 3)
        assert grid.is_cell_visited(1, 3)
        assert grid.is_cell_visited(2, 1)
        assert grid.is_cell_visited(2, 2)
        assert grid.is_cell_visited(2, 3)

    def test_move_down_blocked(self):
        """We should raise a Movement Blocked exception if a move down would collide with an occupied tile"""
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        grid.set_cell_occupied(2, 1, None)
        with pytest.raises(MovementBlocked):
            tetromino.move_down()
        assert grid.is_cell_visited(1, 1)
        assert grid.is_cell_visited(1, 2)
        assert grid.is_cell_visited(1, 3)
        assert grid.is_cell_visited(0, 3)

    def test_move_down_blocked_bottom(self):
        """We should raise a Movement Blocked exception if a move down would collide with the bottom of the grid"""
        grid = Grid(4, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        tetromino.move_down()
        tetromino.move_down()
        with pytest.raises(MovementBlocked):
            tetromino.move_down()
        assert grid.is_cell_visited(3, 1)
        assert grid.is_cell_visited(3, 2)
        assert grid.is_cell_visited(3, 3)
        assert grid.is_cell_visited(2, 3)

    def test_rotate_anticlockwise(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        tetromino.rotate_anticlockwise()
        assert grid.is_cell_visited(0, 1)
        assert grid.is_cell_visited(0, 2)
        assert grid.is_cell_visited(1, 2)
        assert grid.is_cell_visited(2, 2)
        assert not grid.is_cell_visited(1, 1)
        assert not grid.is_cell_visited(1, 3)
        assert not grid.is_cell_visited(0, 3)

    def test_rotate_blocked(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        grid.set_cell_occupied(0, 1, TetrominoColor.RED)
        with pytest.raises(MovementBlocked):
            tetromino.rotate_anticlockwise()
        assert grid.is_cell_visited(1, 1)
        assert grid.is_cell_visited(1, 2)
        assert grid.is_cell_visited(1, 3)
        assert grid.is_cell_visited(0, 3)

    def test_rotate_blocked_edge_of_screen_top(self):
        grid = Grid(5, 5)
        tetromino = TetrominoI(grid, 1, 2, TetrominoColor.RED)
        with pytest.raises(MovementBlocked):
            tetromino.rotate_anticlockwise()

    def test_rotate_blocked_edge_of_screen_bottom(self):
        grid = Grid(2, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        with pytest.raises(MovementBlocked):
            tetromino.rotate_anticlockwise()

    def test_rotate_blocked_edge_of_screen_left(self):
        grid = Grid(5, 5)
        tetromino = TetrominoI(grid, 1, 1, TetrominoColor.RED)
        tetromino.rotate_clockwise()
        with pytest.raises(MovementBlocked):
            tetromino.rotate_clockwise()

    def test_rotate_blocked_edge_of_screen_right(self):
        grid = Grid(5, 5)
        tetromino = TetrominoI(grid, 1, 2, TetrominoColor.RED)
        tetromino.rotate_clockwise()
        tetromino.move_right()
        with pytest.raises(MovementBlocked):
            tetromino.rotate_anticlockwise()

    def test_rotate_clockwise(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        tetromino.rotate_clockwise()
        assert grid.is_cell_visited(0, 2)
        assert grid.is_cell_visited(1, 2)
        assert grid.is_cell_visited(2, 2)
        assert grid.is_cell_visited(2, 3)
        assert not grid.is_cell_visited(1, 1)
        assert not grid.is_cell_visited(1, 3)
        assert not grid.is_cell_visited(0, 3)

    def test_rotate_not_blocked_by_self(self):
        grid = Grid(5, 5)
        tetromino = TetrominoO(grid, 1, 1, TetrominoColor.RED)
        tetromino.rotate_clockwise()
        assert grid.is_cell_visited(1, 0)
        assert grid.is_cell_visited(1, 1)
        assert grid.is_cell_visited(2, 0)
        assert grid.is_cell_visited(2, 1)

    def test_drop_blocked_1(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        grid.set_cell_occupied(4, 1, "red")
        tetromino.drop()
        assert grid.is_cell_occupied(3, 1)
        assert grid.is_cell_occupied(3, 2)
        assert grid.is_cell_occupied(3, 3)
        assert grid.is_cell_occupied(2, 3)
        assert not grid.is_cell_visited(1, 1)
        assert not grid.is_cell_visited(1, 2)
        assert not grid.is_cell_visited(1, 3)
        assert not grid.is_cell_visited(0, 3)

    def test_drop_blocked_bottom(self):
        grid = Grid(5, 5)
        tetromino = TetrominoL(grid, 1, 2, TetrominoColor.RED)
        tetromino.drop()
        assert grid.is_cell_occupied(4, 1)
        assert grid.is_cell_occupied(4, 2)
        assert grid.is_cell_occupied(4, 3)
        assert grid.is_cell_occupied(3, 3)
        assert not grid.is_cell_visited(1, 1)
        assert not grid.is_cell_visited(1, 2)
        assert not grid.is_cell_visited(1, 3)
        assert not grid.is_cell_visited(0, 3)
