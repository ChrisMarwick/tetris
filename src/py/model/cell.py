from dataclasses import dataclass
from enum import Enum


class CellStatus(Enum):
    EMPTY = "EMPTY"  # The cell contains nothing
    VISITED = "VISITED"  # The cell contains a tetromino which is in motion, by making this a separate status to
    # occupied it simplifies some operations where we only want to examine static tetrominos
    OCCUPIED = "OCCUPIED"  # The cell contains a static tetromino


EMPTY_CELL_COLOR = "black"


@dataclass
class Cell:
    status: CellStatus = CellStatus.EMPTY
    color: str = EMPTY_CELL_COLOR
