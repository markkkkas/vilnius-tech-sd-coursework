class Checker:
    def __init__(self, row, column, color):
        self.color = color
        self.row = row
        self.column = column
        self.is_queen = False

    def upgrade_to_queen(self):
        self.is_queen = True
