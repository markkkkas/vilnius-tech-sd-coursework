from .game import Game

import tkinter as tk


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=800, height=800, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.Game = Game()
        self.rows = 8
        self.columns = 8
        self.canvas.bind("<Configure>", self.render_game)
        self.status = tk.Label(self, anchor="w")
        self.status.pack(side="bottom", fill="x")
        self.tile_colors = ['white', 'brown']

    def render_game(self, event=None):
        self.canvas.delete("rect")
        cellwidth = int(self.canvas.winfo_width()/self.columns)
        cellheight = int(self.canvas.winfo_height()/self.columns)
        for row, row_tiles in enumerate(self.Game.board):
            for column, tile in enumerate(row_tiles):
                x1 = column*cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                tile.gui_tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill=tile.color, tags="rect")
                if tile.has_checker():
                    if tile.checker.is_queen:
                        oval = self.canvas.create_oval(x1, y1, x2, y2, fill=tile.checker.color, width = 10)
                        self.canvas.tag_bind(oval, "<1>", lambda event, row=row, column=column: self.set_tile_clicked(row, column))
                    else:
                        oval = self.canvas.create_oval(x1, y1, x2, y2, fill=tile.checker.color)
                        self.canvas.tag_bind(oval, "<1>", lambda event, row=row, column=column: self.set_tile_clicked(row, column))
                self.canvas.tag_bind(tile.gui_tile, "<1>", lambda event, row=row, column=column: self.set_tile_clicked(row, column))

    def set_tile_clicked(self, row, column):
        tile = self.Game.board[row][column].gui_tile
        if self.Game.is_selected():
            selected_tile = self.Game.board[self.Game.selected[0]][self.Game.selected[1]]
            self.Game.move_checker(row, column)
            self.canvas.itemconfigure(selected_tile.gui_tile, fill=selected_tile.color)
            self.render_game()
        else:
            new_color = "yellow" if self.Game.set_selected(row, column) else self.Game.board[row][column].color
            self.canvas.itemconfigure(tile, fill=new_color)
