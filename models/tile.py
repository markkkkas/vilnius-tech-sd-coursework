from .checker import Checker

from typing import Union, List


class Tile:
    tile_colors: List[str] = ['lightcyan2', 'black']

    def __init__(self, row, column, color) -> None:
        self.row: int = row
        self.column: int = column
        self.color: str = color
        self.checker: Union[Checker, None] = None
        self.gui_title = None

    def add_checker(self, piece: Checker) -> None:
        self.checker = piece

    def remove_checker(self) -> Checker:
        removed_checker: Checker = self.checker
        self.checker = None

        return removed_checker

    def has_checker(self) -> Union[Checker, None]:
        return self.checker is not None
