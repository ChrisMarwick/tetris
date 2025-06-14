import logging
from .cell import Cell, CellStatus


class Grid:

    def __init__(self, num_rows=20, num_columns=10):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self._grid = []
        for row in range(self.num_rows):
            self._grid.append([])
            for column in range(self.num_columns):
                self._grid[row].append(Cell())

    def to_dict(self):
        output = []
        for row in range(self.num_rows):
            row_data = []
            for column in range(self.num_columns):
                cell = self._grid[row][column]
                row_data.append({
                    'status': cell.status.name,
                    'color': cell.color.value if cell.color else None
                })
            output.append(row_data)
        return output

    def set_cell_visited(self, row, column, color):
        self._grid[row][column].status = CellStatus.VISITED
        self._grid[row][column].color = color

    def set_cell_occupied(self, row, column, color):
        self._grid[row][column].status = CellStatus.OCCUPIED
        self._grid[row][column].color = color

    def set_cell_empty(self, row, column):
        self._grid[row][column].status = CellStatus.EMPTY
        self._grid[row][column].color = None

    def is_cell_visited(self, row, column):
        return self._grid[row][column].status == CellStatus.VISITED

    def is_cell_occupied(self, row, column):
        return self._grid[row][column].status == CellStatus.OCCUPIED

    def is_row_filled(self, row):
        result = all(self._grid[row][column].status == CellStatus.OCCUPIED for column in range(self.num_columns))
        return result

    def clear_row(self, row_to_clear):
        logging.info(f'Clearing row {row_to_clear}')
        # Clear the row itself
        for column in range(self.num_columns):
            self.set_cell_empty(row_to_clear, column)
        for row in range(row_to_clear - 1, -1, -1):
            for column in range(self.num_columns):
                if not self.is_cell_occupied(row, column):
                    continue
                destination_row = row + 1
                color = self._grid[row][column].color
                self.set_cell_occupied(destination_row, column, color)
                self.set_cell_empty(row, column)

    def __str__(self):
        # '*' chars represent the walls of the grid
        horizontal_wall = '*' * (self.num_columns + 2)
        output = [horizontal_wall]
        for row in range(self.num_rows):
            row_elements = []
            row_elements.append('*')
            for column in range(self.num_columns):
                match self._grid[row][column].status:
                    case CellStatus.OCCUPIED:
                        cell_char = 'x'
                    case CellStatus.VISITED:
                        cell_char = '-'
                    case _:
                        cell_char = ' '
                row_elements.append(cell_char)
            row_elements.append('*')
            output.append(''.join(row_elements))
        output.append(horizontal_wall)
        return '\n'.join(output)
