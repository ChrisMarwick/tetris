import logging
from threading import Timer
from typing import Callable

import keyboard

from game_state import GameState
from high_score import HighScore
from model.grid import Grid
from model.tetromino.tetromino import MovementBlocked
from model.tetromino.tetromino_factory import TetrominoFactory
from game_event import GameEvent
from storage import InMemoryStorage


file_handler = logging.FileHandler("server.log")
logging.basicConfig(level=logging.INFO, handlers=[file_handler])

logger = logging.getLogger(__name__)

NUM_ROWS = 20
NUM_COLUMNS = 10
INITIAL_GRAVITY_INTERVAL = 0.5  # seconds
TETROMINO_SPAWN_POSITION = (2, NUM_COLUMNS // 2)
ROW_CLEAR_SCORING = {1: 40, 2: 100, 3: 300, 4: 1200}


class Game:
    """
    Handles the main event loop and game logic
    """

    def __init__(self, event_callback):
        logger.info("*** Starting game...")
        self.grid = Grid(NUM_ROWS, NUM_COLUMNS)
        self.tetromino_factory = TetrominoFactory(self.grid)
        self.active_tetromino = self.create_tetromino()
        self.game_state = GameState.PAUSED
        self.score = 0
        self.current_level_rows_cleared = 0
        self.level = 1
        self.event_callback = event_callback
        self.gravity_interval = INITIAL_GRAVITY_INTERVAL
        storage = InMemoryStorage()
        self.high_score = HighScore(storage)
        self.is_high_score = False

    def create_tetromino(self):
        try:
            new_tetromino = self.tetromino_factory.create_tetromino(
                *TETROMINO_SPAWN_POSITION
            )
            logging.info("Creating new tetromino %s", new_tetromino)
        except MovementBlocked:
            # If creating a new tetromino is blocked by existing tetrominos then the game ends
            self.game_state = GameState.ENDED
            high_score_index = self.high_score.check_and_insert_score("X", self.score)
            if high_score_index != -1:
                self.is_high_score = True
            self.dispatch_event(GameEvent.GAME_ENDED)
            return None
        return new_tetromino

    @classmethod
    def keyboard_action(cls, action: Callable[[], None]):
        try:
            action()
        except MovementBlocked:
            pass

    def to_dict(self):
        return {
            "grid": self.grid.to_dict(),
            "score": self.score,
            "level": self.level,
            "game_state": self.game_state.value,
            "is_high_score": self.is_high_score,
        }

    def dispatch_event(self, event: GameEvent, data: dict = None):
        if event == GameEvent.GRAVITY_TICK:
            self._handle_gravity_tick()
        elif event == GameEvent.TOGGLE_PAUSE:
            self._handle_toggle_pause()
        elif event == GameEvent.DROP:
            self.active_tetromino.drop()
        elif event == GameEvent.ROTATE_ANTICLOCKWISE:
            self.keyboard_action(self.active_tetromino.rotate_anticlockwise)
        elif event == GameEvent.ROTATE_CLOCKWISE:
            self.keyboard_action(self.active_tetromino.rotate_clockwise)
        elif event == GameEvent.MOVE_LEFT:
            self.keyboard_action(self.active_tetromino.move_left)
        elif event == GameEvent.MOVE_RIGHT:
            self.keyboard_action(self.active_tetromino.move_right)
        self.event_callback(event, data or self.to_dict())

    def _check_for_cleared_rows(self):
        num_cleared_rows = 0
        for row in range(self.grid.num_rows):
            if self.grid.is_row_filled(row):
                self.grid.clear_row(row)
                num_cleared_rows += 1
                self.dispatch_event(GameEvent.ROW_CLEARED, {"row": row})
        if num_cleared_rows:
            awarded_score = ROW_CLEAR_SCORING[num_cleared_rows]
            self.score += awarded_score
            self.dispatch_event(
                GameEvent.SCORE,
                {"number_rows": num_cleared_rows, "score": awarded_score},
            )
            self.current_level_rows_cleared += num_cleared_rows
            self._update_level()

    def _update_level(self):
        if self.current_level_rows_cleared >= 10:
            self.current_level_rows_cleared -= 10
            self.level += 1
            self.gravity_interval = self.gravity_interval - (
                0.2 * self.gravity_interval
            )
            self.dispatch_event(GameEvent.LEVEL_ADVANCE, {"level": self.level})

    def _handle_gravity_tick(self):
        try:
            self.active_tetromino.move_down()
        except MovementBlocked:
            logger.info("Tetromino blocked, spawning new tetromino")
            self.active_tetromino.lock()
            self._check_for_cleared_rows()
            self.active_tetromino = self.create_tetromino()
            logger.info("Lock and spawn finished")

    def _handle_toggle_pause(self):
        if self.game_state == GameState.PAUSED:
            self.start()
        elif self.game_state == GameState.IN_PROGRESS:
            self.stop()

    def gravity_loop(self):
        if self.game_state in (GameState.PAUSED, GameState.ENDED):
            return
        Timer(self.gravity_interval, self.gravity_loop).start()
        self.dispatch_event(GameEvent.GRAVITY_TICK)

    def start(self):
        if self.game_state == GameState.ENDED:
            return

        logger.info("Starting/unpausing game")
        self.game_state = GameState.IN_PROGRESS
        self.gravity_loop()

    def stop(self):
        if self.game_state == GameState.ENDED:
            return
        logger.info("Pausing game")
        self.game_state = GameState.PAUSED


if __name__ == "__main__":
    game = Game(lambda event, game_state: print(game_state["grid"]))
    keyboard.on_press_key("a", lambda _: game.dispatch_event(GameEvent.MOVE_LEFT))
    keyboard.on_press_key("d", lambda _: game.dispatch_event(GameEvent.MOVE_RIGHT))
    keyboard.on_press_key(
        "q", lambda _: game.dispatch_event(GameEvent.ROTATE_ANTICLOCKWISE)
    )
    keyboard.on_press_key(
        "e", lambda _: game.dispatch_event(GameEvent.ROTATE_CLOCKWISE)
    )
    keyboard.on_press_key("s", lambda _: game.dispatch_event(GameEvent.DROP))
    keyboard.on_press_key("p", lambda _: game.dispatch_event(GameEvent.TOGGLE_PAUSE))
    game.start()
