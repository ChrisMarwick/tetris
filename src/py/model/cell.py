from dataclasses import dataclass
from enum import Enum


class CellStatus(Enum):
    EMPTY = 0       # The cell contains nothing
    VISITED = 1     # The cell contains a tetromino which is in motion, by making this a separate status to occupied 
                    # it simplifies some operations where we only want to examine static tetrominos
    OCCUPIED = 2    # The cell contains a static tetromino


class CellColor(Enum):
    RED = 'RED'
    ORANGE = 'ORANGE'
    YELLOW = 'YELLOW'
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    PURPLE = 'PURPLE'


@dataclass
class Cell:
    status: CellStatus = CellStatus.EMPTY
    color: CellColor = None
