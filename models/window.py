from models.game import Game

import tkinter as tk


class Window(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        self.rows: int = 8
        self.columns: int = 8
        self.checker_radius: int = 5

        self.game: Game = Game(self.rows, self.columns)

        self.active_window: tk.Canvas = tk.Canvas(
            self,
            width=self.columns * 100,
            height=self.rows * 100,
            borderwidth=0,
            highlightthickness=0,
        )
        self.active_window.pack(side="top", fill="both", expand="true")
        self.active_window.bind("<Configure>", self.render_game)

    def recalculate_cell(self):
        self.active_window.delete("rect")
        return int(self.active_window.winfo_width() / self.columns), int(
            self.active_window.winfo_height() / self.columns
        )

    def attach_click_event(self, item, row, column):
        self.active_window.tag_bind(
            item,
            "<1>",
            lambda _event, _row=row, _column=column: self.set_tile_clicked(
                _row, _column
            ),
        )

    def render_game(self, event=None) -> None:
        cellwidth, cellheight = self.recalculate_cell()

        for row, row_tiles in enumerate(self.game.board):
            for column, tile in enumerate(row_tiles):
                x1, y1 = column * cellwidth, row * cellheight
                x2, y2 = x1 + cellwidth, y1 + cellheight

                tile.gui_tile = self.active_window.create_rectangle(
                    x1, y1, x2, y2, fill=tile.get_color(), tags="rect"
                )

                self.attach_click_event(tile.gui_tile, row, column)

                if tile.has_checker():
                    color = tile.get_checker().get_color()
                    width = (
                        self.checker_radius if tile.get_checker().is_queen() else None
                    )

                    checker = self.active_window.create_oval(
                        x1 + self.checker_radius,
                        y1 + self.checker_radius,
                        x2 - self.checker_radius,
                        y2 - self.checker_radius,
                        fill=color,
                        width=width,
                    )
                    self.attach_click_event(checker, row, column)

    def set_tile_clicked(self, row, column) -> None:
        if self.game.is_selected():
            selected_tile = self.game.board[self.game.selected[0]][
                self.game.selected[1]
            ]
            self.game.move_checker(row, column)
            self.active_window.itemconfigure(
                selected_tile.gui_tile, fill=selected_tile.get_color()
            )
            self.render_game()
        else:
            new_color = (
                "yellow"
                if self.game.set_selected(row, column)
                else self.game.board[row][column].get_color()
            )
            self.active_window.itemconfigure(
                self.game.board[row][column].gui_tile, fill=new_color
            )
