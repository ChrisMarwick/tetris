from enum import Enum


class GameState(Enum):
    """
    Different states the game can be in.
    """

    IN_PROGRESS = "IN_PROGRESS"     # Game loop is active and stuff is happening
    PAUSED = "PAUSED"               # Game loop is temporarily paused, no events are processed
    ENDED = "ENDED"                 # Game is finished, all events are disabled
