class Checker:
    def __init__(self, row: int, column: int, color: str) -> None:
        self.row: int = row
        self.column: int = column
        self.color: str = color
        self.is_queen: bool = False

    def upgrade_to_queen(self) -> None:
        self.is_queen = True
