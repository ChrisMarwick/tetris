import random

from pytest_mock import MockerFixture

from model.grid import Grid
from model.tetromino.tetromino import TetrominoI, TetrominoColor
from model.tetromino.tetromino_factory import TetrominoFactory


class TestTetrominoFactory:
    """Tests for the tetromino factory"""

    def test_create_tetromino(self, mocker: MockerFixture):
        """
        Mocking the random element to pick a red I tetromino with one rotation, ensure that the resultant tetromino is
        as we expected.
        """
        with mocker.patch.object(
            random, "randint", return_value=1
        ), mocker.patch.object(
            TetrominoFactory, "_create_tetromino_bag", return_value=[TetrominoI]
        ), mocker.patch.object(
            random, "choice", return_value=TetrominoColor.RED
        ):
            grid = Grid()
            tetromino = TetrominoFactory(grid).create_tetromino(1, 5)
        assert tetromino.color == TetrominoColor.RED
        assert isinstance(tetromino, TetrominoI)
        assert tetromino.relative_cell_positions == [(0, 0), (-1, 0), (1, 0), (2, 0)]
