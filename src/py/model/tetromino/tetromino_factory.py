import logging
import random
from model.tetromino.tetromino import (
    TetrominoI,
    TetrominoJ,
    TetrominoL,
    TetrominoO,
    TetrominoS,
    TetrominoT,
    TetrominoZ,
    TetrominoColor,
)


class TetrominoFactory:
    """
    Factory class that abstracts the various rules around tetromino creation away from the client.
    """

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
        bag = [
            TetrominoI,
            TetrominoJ,
            TetrominoL,
            TetrominoO,
            TetrominoS,
            TetrominoT,
            TetrominoZ,
        ]
        random.shuffle(bag)
        return bag

    def create_tetromino(self, start_row, start_column):
        """
        Create a random tetromino from the bag of available tetrominos with a random color, then rotate it randomly
        between 0 and 3 times (covering all 4 rotational permutations).
        """
        if not self.current_bag:
            self.current_bag = self._create_tetromino_bag()
        # pylint: disable-next=invalid-name     # The variable holds a class so should use an appropriate name
        TetrominoCls = self.current_bag.pop()
        logging.info("Creating tetromino %s", TetrominoCls)

        random_color = random.choice(list(TetrominoColor))

        tetromino = TetrominoCls(self.grid, start_row, start_column, random_color)

        random_rotation = random.randint(0, 3)
        for _ in range(random_rotation):
            tetromino.rotate_clockwise()
        return tetromino
