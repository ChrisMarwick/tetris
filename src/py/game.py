import logging
import keyboard
from threading import Timer
from model.grid import Grid
from model.tetromino.tetromino import MovementBlocked
from model.tetromino.tetromino import TetrominoFactory
from game_event import GameEvent

file_handler = logging.FileHandler('server.log')
logging.basicConfig(level=logging.INFO, handlers=[file_handler])

NUM_ROWS = 20
NUM_COLUMNS = 10
GRAVITY_INTERVAL = 0.5 # seconds
TETROMINO_SPAWN_POSITION = (1, NUM_COLUMNS // 2)


class Game:

    def __init__(self, event_callback=None):
        logging.info('*** Starting game...')
        self.grid = Grid(NUM_ROWS, NUM_COLUMNS)
        self.tetromino_factory = TetrominoFactory(self.grid)
        self.active_tetromino = self.create_tetromino()
        self.event_callback = event_callback
        self.is_paused = True

    def create_tetromino(self):
        # TODO: should be a random tetromino
        try:
            new_tetromino = self.tetromino_factory.create_tetromino(*TETROMINO_SPAWN_POSITION)
        except MovementBlocked:
            # If creating a new tetromino is blocked by existing tetrominos then the game ends
            raise Exception('Game ended')
        return new_tetromino

    @classmethod
    def keyboard_action(cls, action):
        try:
            logging.info(f'Action {action} on active tetromino')
            action()
        except MovementBlocked:
            pass

    def to_dict(self):
        # print(self.grid)
        return {
            'grid': self.grid.to_dict()
            # 'active_tetromino': self.active_tetromino
        }

    def dispatch_event(self, event: GameEvent):
        # print('Received event:', event)
        if event == GameEvent.GRAVITY_TICK:
            self._handle_gravity_tick()
        elif event == GameEvent.TOGGLE_PAUSE:
            self._handle_toggle_pause()
        elif event == GameEvent.END:
            self.is_paused = True
        elif event == GameEvent.DROP:
            self.active_tetromino.drop()
        elif event == GameEvent.ROTATE_ANTICLOCKWISE:
            self.active_tetromino.rotate_anticlockwise()
        elif event == GameEvent.ROTATE_CLOCKWISE:
            self.active_tetromino.rotate_clockwise()
        elif event == GameEvent.MOVE_LEFT:
            self.active_tetromino.move_left()
        elif event == GameEvent.MOVE_RIGHT:
            self.active_tetromino.move_right()
        else:
            logging.error(f'Unknown event: {event}')
            return
        if self.event_callback:
            self.event_callback(event, self.to_dict())

    def _check_for_cleared_rows(self):
        num_cleared_rows = 0
        for row in range(self.grid.num_rows - 1, -1, -1):
            if self.grid.is_row_filled(row):
                self.grid.clear_row(row)
                num_cleared_rows += 1

    def _handle_gravity_tick(self):
        try:
            logging.info('Moving active tetromino down by 1')
            self.active_tetromino.move_down()
        except MovementBlocked:
            logging.info('Tetromino blocked, spawning new tetromino')
            self.active_tetromino.lock()
            self._check_for_cleared_rows()
            self.active_tetromino = self.create_tetromino()
            logging.info('Lock and spawn finished')

    def _handle_toggle_pause(self):
        if self.is_paused:
            self.start()
        else:
            self.stop()

    def gravity_loop(self):
        if self.is_paused:
            return
        Timer(GRAVITY_INTERVAL, self.gravity_loop).start()
        self.dispatch_event(GameEvent.GRAVITY_TICK)

    def start(self):
        self.is_paused = False
        self.gravity_loop()

    def stop(self):
        self.is_paused = True


if __name__ == '__main__':
    game = Game(lambda event, game_state: print(game_state['grid']))
    keyboard.on_press_key('a', lambda _: game.dispatch_event(GameEvent.MOVE_LEFT))
    keyboard.on_press_key('d', lambda _: game.dispatch_event(GameEvent.MOVE_RIGHT))
    keyboard.on_press_key('q', lambda _: game.dispatch_event(GameEvent.ROTATE_ANTICLOCKWISE))
    keyboard.on_press_key('e', lambda _: game.dispatch_event(GameEvent.ROTATE_CLOCKWISE))
    keyboard.on_press_key('s', lambda _: game.dispatch_event(GameEvent.DROP))
    keyboard.on_press_key('p', lambda _: game.dispatch_event(GameEvent.TOGGLE_PAUSE))
    game.start()
