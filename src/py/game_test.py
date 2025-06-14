from game import Game
from game_state import GameState
from model.grid import Grid
from pytest_mock import MockerFixture


class TestGame:

    def test_start_from_paused(self, mocker: MockerFixture):
        """If the game is paused then start should unpause it and invoke the gravity loop"""
        grid = Grid()
        game = Game(grid)
        gravity_loop_mock = mocker.patch.object(Game, 'gravity_loop')

        game.start()
        assert game.game_state == GameState.IN_PROGRESS
        assert gravity_loop_mock.call_count == 1

    def test_start_from_ended(self, mocker: MockerFixture):
        grid = Grid()
        game = Game(grid)
        game.game_state = GameState.ENDED

        game.start()
        assert game.game_state == GameState.ENDED

    def test_stop_from_in_progress(self):
        grid = Grid()
        game = Game(grid)
        game.game_state = GameState.IN_PROGRESS

        game.stop()
        assert game.game_state == GameState.PAUSED

    def test_stop_from_ended(self):
        grid = Grid()
        game = Game(grid)
        game.game_state = GameState.ENDED

        game.stop()
        assert game.game_state == GameState.ENDED
