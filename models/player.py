from typing import List

import tkinter


class Player:
    def __init__(self, name: str, tiles: List, position: str):
        self.name = name
        self.tiles = tiles
        self.position = position

    @staticmethod
    def move_checker(event, arg):
        print(arg)

    def render_checkers(self, active_window):
        for tile in self.tiles:
            checker = tkinter.Canvas(active_window, width=40, height=40,
                                     background="red" if self.position == "bot" else "white", highlightthickness=0)
            checker.bind("<Button-1>", lambda event, arg=tile: self.move_checker(event, arg))
            checker.grid(row=tile.row, column=tile.column)
