from .cell import Cell


class Grid:

    def __init__(self, num_rows=20, num_columns=10):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self._grid = []
        # self._columns_lowest_unoccupied_cell = []
        for row in range(self.num_rows):
            self._grid.append([])
            for column in range(self.num_columns):
                self._grid[row].append(Cell())
        # for column in range(self.num_columns):
        #     self._columns_lowest_unoccupied_cell.append(self.num_rows - 1)

    def set_cell_occupied(self, row, column, color):
        self._grid[row][column].is_occupied = True
        self._grid[row][column].color = color
        # self._columns_lowest_unoccupied_cell[column] = min(row, self._columns_lowest_unoccupied_cell[column])

    def set_cell_unoccupied(self, row, column):
        self._grid[row][column].is_occupied = False
        self._grid[row][column].color = None
        # for r in range(self.num_rows):
        #     if self._grid[r][column].is_occupied:
        #         self._columns_lowest_unoccupied_cell[column] = r
        #         return
        # self._columns_lowest_unoccupied_cell[column] = self.num_rows - 1

    def is_cell_occupied(self, row, column):
        return self._grid[row][column].is_occupied

    def is_row_filled(self, row):
        return all(self._grid[row][column].is_occupied for column in range(self.num_columns))

    def clear_row(self, row_to_clear):
        # Clear the row itself
        for column in range(self.num_columns):
            self.set_cell_unoccupied(row_to_clear, column)
        # TODO: rather than moving down by 1 row it should move down until it hits the floor/an occupied tile, 
        # whilst being connected to tiles of the same tetromino with flood fill rules. 
        for column in range(self.num_columns):
            for row in range(row_to_clear - 1, -1, -1):
                if not self.is_cell_occupied(row, column):
                    continue
                destination_row = row + 1
                color = self._grid[row][column].color
                self.set_cell_occupied(destination_row, column, color)
                self.set_cell_unoccupied(row, column)
            # We know for certain that the lowest unoccupied cell in each column will go down by 1
            # self._columns_lowest_unoccupied_cell[column] += 1

    def __str__(self):
        output = []
        for row in range(self.num_rows):
            row_elements = []
            for column in range(self.num_columns):
                row_elements.append('x' if self._grid[row][column].is_occupied else ' ')
            output.append(''.join(row_elements))
        return '\n'.join(output)
