from enum import Enum


class GameEvent(Enum):

    GRAVITY_TICK = 'GRAVITY_TICK'
    TOGGLE_PAUSE = 'TOGGLE_PAUSE'
    END = 'END'

    DROP = 'DROP'  # Drop the active tetromino to the bottom of the grid

    # Movement/Rotation Events
    MOVE_LEFT = 'MOVE_LEFT'  # Move the active tetromino left
    MOVE_RIGHT = 'MOVE_RIGHT'  # Move the active tetromino right
    ROTATE_CLOCKWISE = 'ROTATE_CLOCKWISE'  # Rotate the active tetromino clockwise
    ROTATE_ANTICLOCKWISE = 'ROTATE_ANTICLOCKWISE'  # Rotate the active tetromino anticlockwise
