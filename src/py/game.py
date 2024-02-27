import keyboard
from threading import Timer
from model.grid import Grid
from model.tetromino.tetromino import MovementBlocked
from model.tetromino.tetromino_l import TetrominoL


NUM_ROWS = 20
NUM_COLUMNS = 10
TIMER_INTERVAL = 0.5

def create_tetromino():
    # TODO: should be a random tetromino
    try:
        new_tetromino = TetrominoL(grid, *tetromino_spawn_position)
    except MovementBlocked:
        # If creating a new tetromino is blocked by existing tetrominos then the game ends
        raise Exception('Game ended')
    return new_tetromino


grid = Grid(NUM_ROWS, NUM_COLUMNS)
tetromino_spawn_position = (0, NUM_COLUMNS // 2)
active_tetromino = create_tetromino()

def keyboard_action(action):
    try:
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
        active_tetromino.move_down()
    except MovementBlocked:
        active_tetromino = create_tetromino()
    except Exception:
        print('Yay!')
    print(grid)

Timer(TIMER_INTERVAL, game_loop).start()
