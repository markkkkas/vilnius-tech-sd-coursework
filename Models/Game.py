import tkinter


class Game:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
        self.active_window = None

    def start_new_game(self):
        self._render_table()

    def _render_table(self):
        self.active_window = tkinter.Tk()
        self.active_window.title("Checkers")
        self.active_window.geometry(f'{self.length * 100}x{self.width * 100}')

        # Painting rectangles
        black_spot = tkinter.Canvas(self.active_window, width=100, height=100)
        black_spot.pack()
        black_spot.create_rectangle(0, 0, 800, 800, fill="black")

        self.active_window.mainloop()
