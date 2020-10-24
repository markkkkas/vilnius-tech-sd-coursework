from models.player import Player
from models.tile import Tile

import tkinter
import random


class Game:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
        self.active_window = None
        self.player_1 = None
        self.player_2 = None
        self.available_tiles = {"top_tiles": [], "bottom_tiles": []}

    def start_new_game(self):
        self.render_table()

        self.player_1 = Player("Player_1", self.available_tiles["top_tiles"], position="top")
        self.player_2 = Player("Player_2", self.available_tiles["bottom_tiles"], position="bot")

        self.player_1.render_checkers(self.active_window)
        self.player_2.render_checkers(self.active_window)

        while True:
            self.active_window.update()

    def update_available_tiles(self, i, y):
        if i <= (self.width / 2) - 2:
            self.available_tiles["top_tiles"].append(Tile(row=i, column=y))
        elif i > (self.width / 2):
            self.available_tiles["bottom_tiles"].append(Tile(row=i, column=y))

    def render_table(self):
        self.active_window = tkinter.Tk()
        self.active_window.title("Checkers")
        self.active_window.geometry(f'{self.length * 104}x{self.width * 104}')

        for i in range(0, self.width):
            for y in range(0, self.length):
                black_tile = tkinter.Canvas(self.active_window, width=100, height=100, background="black")
                white_tile = tkinter.Canvas(self.active_window, width=100, height=100, background="white")

                if y % 2 == 0:
                    if i % 2 == 0:
                        white_tile.grid(row=i, column=y)
                    else:
                        black_tile.grid(row=i, column=y)
                        self.update_available_tiles(i, y)
                else:
                    if i % 2 == 0:
                        black_tile.grid(row=i, column=y)
                        self.update_available_tiles(i, y)
                    else:
                        white_tile.grid(row=i, column=y)
