from typing import Tuple


class Checker:
    def __init__(self, row: int, column: int, color: str) -> None:
        self.__row: int = row
        self.__column: int = column
        self.__color: str = color
        self.__queen: bool = False

    def upgrade_to_queen(self) -> None:
        self.__queen = True

    def is_queen(self) -> bool:
        return self.__queen is True

    def get_coords(self) -> Tuple[int, int]:
        return self.__row, self.__column

    def get_color(self) -> str:
        return self.__color

    def set_coords(self, row: int, column: int) -> None:
        self.__row = row
        self.__column = column

    def set_color(self, color: str) -> None:
        self.__color = color
