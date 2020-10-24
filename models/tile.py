class Tile:
    tile_colors = ['white', 'black']

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.checker = None

    def add_checker(self, piece):
        self.checker = piece

    def remove_checker(self):
        removed_checker = self.checker
        self.checker = None

        return removed_checker

    def has_checker(self):
        return self.checker is not None
