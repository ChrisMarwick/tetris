from dataclasses import dataclass


@dataclass
class Cell:
    is_occupied = False
    color = None
