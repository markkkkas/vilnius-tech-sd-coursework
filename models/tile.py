from models.checker import Checker
from typing import Tuple, List, Optional


class Tile:
    tile_colors: List[str] = ["lightcyan2", "black"]

    def __init__(self, row, column, color) -> None:
        self.__row: int = row
        self.__column: int = column
        self.__color: str = color
        self.__checker: Optional[Checker] = None

    def add_checker(self, piece: Checker) -> None:
        self.__checker = piece

    def remove_checker(self) -> Checker:
        removed_checker: Checker = self.__checker
        self.__checker = None

        return removed_checker

    def has_checker(self) -> bool:
        return self.__checker is not None

    def get_checker(self) -> Optional[Checker]:
        return self.__checker

    def set_coords(self, row: int, column: int) -> None:
        self.__row = row
        self.__column = column

    def get_coords(self) -> Tuple[int, int]:
        return self.__row, self.__column

    def get_color(self) -> str:
        return self.__color

    def set_color(self, color: str) -> None:
        self.__color = color
