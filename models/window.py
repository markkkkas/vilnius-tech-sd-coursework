from .game import Game

import tkinter as tk


class Window(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        print(*args, **kwargs)

        self.rows: int = 8
        self.columns: int = 8

        self.game: Game = Game()

        self.active_window: tk.Canvas = tk.Canvas(
            self,
            width=self.columns * 100,
            height=self.rows * 100,
            borderwidth=0,
            highlightthickness=0,
        )
        self.active_window.pack(side="top", fill="both", expand="true")
        self.active_window.bind("<Configure>", self.render_game)

    def render_game(self, event=None) -> None:
        self.active_window.delete("rect")

        cellwidth = int(self.active_window.winfo_width() / self.columns)
        cellheight = int(self.active_window.winfo_height() / self.columns)

        for row, row_tiles in enumerate(self.game.board):
            for column, tile in enumerate(row_tiles):
                x1 = column * cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight

                tile.gui_tile = self.active_window.create_rectangle(
                    x1, y1, x2, y2, fill=tile.color, tags="rect"
                )

                if tile.has_checker():
                    if tile.checker.is_queen:
                        _checker = self.active_window.create_oval(
                            x1 + 5,
                            y1 + 5,
                            x2 - 5,
                            y2 - 5,
                            fill=tile.checker.color,
                            width=5,
                        )
                        self.active_window.tag_bind(
                            _checker,
                            "<1>",
                            lambda _event, _row=row, _column=column: self.set_tile_clicked(
                                _row, _column
                            ),
                        )
                    else:
                        _checker = self.active_window.create_oval(
                            x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=tile.checker.color
                        )
                        self.active_window.tag_bind(
                            _checker,
                            "<1>",
                            lambda _event, _row=row, _column=column: self.set_tile_clicked(
                                _row, _column
                            ),
                        )

                self.active_window.tag_bind(
                    tile.gui_tile,
                    "<1>",
                    lambda _event, _row=row, _column=column: self.set_tile_clicked(
                        _row, _column
                    ),
                )

    def set_tile_clicked(self, row, column) -> None:
        tile = self.game.board[row][column].gui_tile

        if self.game.is_selected():
            selected_tile = self.game.board[self.game.selected[0]][
                self.game.selected[1]
            ]
            self.game.move_checker(row, column)
            self.active_window.itemconfigure(
                selected_tile.gui_tile, fill=selected_tile.color
            )
            self.render_game()
        else:
            new_color = (
                "yellow"
                if self.game.set_selected(row, column)
                else self.game.board[row][column].color
            )
            self.active_window.itemconfigure(tile, fill=new_color)
