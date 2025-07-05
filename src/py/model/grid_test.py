from .grid import Grid


class TestGrid:
    """Tests on the Grid class"""

    def test_set_cell_occupied(self):
        grid = Grid(2, 2)
        grid.set_cell_occupied(0, 1, None)
        assert grid.is_cell_occupied(0, 1) is True

    def test_set_cell_empty(self):
        grid = Grid(2, 2)
        grid.set_cell_occupied(0, 1, None)
        grid.set_cell_empty(0, 1)
        assert grid.is_cell_occupied(0, 1) is False

    def test_is_row_filled(self):
        grid = Grid(2, 3)
        grid.set_cell_occupied(1, 0, None)
        grid.set_cell_occupied(1, 1, None)
        grid.set_cell_occupied(1, 2, None)
        assert not grid.is_row_filled(0)
        assert grid.is_row_filled(1)

    def test_clear_row(self):
        grid = Grid(4, 2)
        grid.set_cell_occupied(0, 0, None)
        grid.set_cell_occupied(1, 0, None)
        grid.set_cell_occupied(1, 1, None)
        grid.set_cell_occupied(2, 0, None)
        grid.set_cell_occupied(3, 0, None)
        grid.clear_row(2)
        assert not grid.is_cell_occupied(0, 0)
        assert not grid.is_cell_occupied(0, 1)
        assert grid.is_cell_occupied(1, 0)
        assert not grid.is_cell_occupied(1, 1)
        assert grid.is_cell_occupied(2, 0)
        assert grid.is_cell_occupied(2, 1)
        assert grid.is_cell_occupied(3, 0)
        assert not grid.is_cell_occupied(3, 1)

    def test__str__(self):
        grid = Grid(3, 5)
        grid.set_cell_occupied(0, 0, None)
        grid.set_cell_occupied(0, 1, None)
        grid.set_cell_occupied(0, 2, None)
        grid.set_cell_occupied(2, 4, None)
        assert str(grid) == "*******\n" "*xxx  *\n" "*     *\n" "*    x*\n" "*******"
