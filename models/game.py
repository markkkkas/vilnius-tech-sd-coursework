from models.tile import Tile
from models.checker import Checker

from typing import List, Tuple, Optional


class Game:
    checker_colors = ["white", "red"]

    def __init__(self, rows: int, columns: int) -> None:
        self.players: List[str] = ["red", "white"]
        self.selected: Tuple[Optional[int, int]] = (None, None)
        self.board: List[Tile] = []
        self.turn: int = 0

        self.rows: int = rows
        self.columns: int = columns

        for r_index in range(rows):
            row: List[Tile] = []

            for c_index in range(columns):
                tile: Tile = Tile(
                    r_index, c_index, Tile.tile_colors[(r_index + c_index) % 2]
                )

                if tile.get_color() == Tile.tile_colors[1]:
                    if r_index in range(0, (self.rows // 2) - 1):
                        checker: Checker = Checker(
                            r_index, c_index, self.checker_colors[0]
                        )
                        tile.add_checker(checker)

                    if r_index in range((self.rows // 2) + 1, self.rows):
                        checker: Checker = Checker(
                            r_index, c_index, self.checker_colors[1]
                        )
                        tile.add_checker(checker)

                row.append(tile)
            self.board.append(row)

    def exit_game(self) -> bool:
        white, red = 0, 0
        for row in self.board:
            for tile in row:
                if tile.has_checker():
                    if tile.get_checker().get_color() == "white":
                        white = white + 1
                    else:
                        red = red + 1

        return white == 0 or red == 0

    def set_next_turn(self) -> None:
        self.turn = (self.turn + 1) % 2

    def is_selected(self) -> bool:
        return self.selected != (None, None)

    def set_selected(self, row: int, col: int) -> bool:
        if self.board[row][col].has_checker():
            checker = self.board[row][col].get_checker()

            if checker.get_color() == self.players[self.turn]:
                self.selected = (row, col)
                return True
            else:
                self.selected = (None, None)

        return False

    def move_checker(self, row: int, col: int) -> None:
        cur_row: Optional[int] = self.selected[0]
        cur_col: Optional[int] = self.selected[1]

        checker = self.board[cur_row][cur_col].get_checker()

        max_valid_moves = [
            (cur_row + i, cur_col + j)
            for i in [-1 if self.turn == 0 else 1]
            for j in [-1, 1]
        ]
        max_valid_attacks = [
            (cur_row + i, cur_col + j)
            for i in [-2 if self.turn == 0 else 2]
            for j in [-2, 2]
        ]

        max_valid_moves = [
            pos for pos in max_valid_moves if pos[0] in range(8) and pos[1] in range(8)
        ]

        max_valid_attacks = [
            pos
            for pos in max_valid_attacks
            if pos[0] in range(8) and pos[1] in range(8)
        ]

        max_valid_moves = [
            pos
            for pos in max_valid_moves
            if not self.board[pos[0]][pos[1]].has_checker()
        ]
        max_valid_attacks = [
            pos
            for pos in max_valid_attacks
            if not self.board[pos[0]][pos[1]].has_checker()
        ]

        new_valid: List = []
        for pos in max_valid_attacks:
            tile: Tile = self.board[int((cur_row + pos[0]) // 2)][
                int((cur_col + pos[1]) // 2)
            ]
            if (
                tile.has_checker()
                and tile.get_checker().get_color() != checker.get_color()
            ):
                new_valid.append(pos)

        max_valid_attacks = new_valid

        if (row, col) in max_valid_moves or (row, col) in max_valid_attacks:
            moved_piece: Optional[Checker] = self.board[cur_row][
                cur_col
            ].remove_checker()
            moved_piece.row = row
            moved_piece.col = col

            if moved_piece.get_color() == self.players[0]:
                if moved_piece.row == 0:
                    moved_piece.upgrade_to_queen()
            elif moved_piece.get_color() == self.players[1]:
                if moved_piece.row == 7:
                    moved_piece.upgrade_to_queen()

            self.board[row][col].add_checker(moved_piece)

            if (row, col) in max_valid_moves:
                self.set_next_turn()
            elif (row, col) in max_valid_attacks:
                self.board[int((row + cur_row) // 2)][
                    int((col + cur_col) // 2)
                ].remove_checker()

        self.selected = (None, None)

        if self.exit_game():
            exit()
