import logging
import keyboard
from threading import Timer
from model.grid import Grid
from model.tetromino.tetromino import MovementBlocked
from model.tetromino.tetromino import TetrominoFactory


file_handler = logging.FileHandler('server.log')
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler])

NUM_ROWS = 20
NUM_COLUMNS = 10
TIMER_INTERVAL = 0.5

def create_tetromino():
    # TODO: should be a random tetromino
    try:
        new_tetromino = tetromino_factory.create_tetromino(*tetromino_spawn_position)
    except MovementBlocked:
        # If creating a new tetromino is blocked bys existing tetrominos then the game ends
        raise Exception('Game ended')
    return new_tetromino


logging.info('*** Starting game...')
grid = Grid(NUM_ROWS, NUM_COLUMNS)
tetromino_factory = TetrominoFactory(grid)
tetromino_spawn_position = (1, NUM_COLUMNS // 2)
active_tetromino = create_tetromino()

def keyboard_action(action):
    try:
        logging.info(f'Action {action} on active tetromino')
        action()
    except MovementBlocked:
        pass

keyboard.on_press_key('a', lambda _: keyboard_action(active_tetromino.move_left))
keyboard.on_press_key('d', lambda _: keyboard_action(active_tetromino.move_right))
keyboard.on_press_key('q', lambda _: keyboard_action(active_tetromino.rotate_anticlockwise))
keyboard.on_press_key('e', lambda _: keyboard_action(active_tetromino.rotate_clockwise))
keyboard.on_press_key('s', lambda _: keyboard_action(active_tetromino.drop))

def game_loop():
    global active_tetromino
    Timer(TIMER_INTERVAL, game_loop).start()
    try:
        logging.info('Moving active tetromino down by 1')
        active_tetromino.move_down()
    except MovementBlocked:
        logging.info('Tetromino blocked, spawning new tetromino')
        active_tetromino.lock()
        active_tetromino = create_tetromino()
        logging.info('Lock and spawn finished')
    row_to_check = grid.num_rows - 1
    while grid.is_row_filled(row_to_check):
        grid.clear_row(row_to_check)
        row_to_check -= 1
    print(grid)

Timer(TIMER_INTERVAL, game_loop).start()
