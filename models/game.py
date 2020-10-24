from .tile import Tile
from .checker import Checker

from typing import Union, List, Tuple


class Game:
    def __init__(self) -> None:
        self.players: List[str] = ['red', 'white']
        self.selected: Tuple[Union[None, int], Union[None, int]] = (None, None)
        self.board: Union[List, Tile] = []
        self.turn: int = 0

        for r_index in range(8):
            row: List[Tile] = []

            for c_index in range(8):
                tile: Tile = Tile(r_index, c_index, Tile.tile_colors[(r_index + c_index) % 2])

                if tile.color == Tile.tile_colors[1]:
                    if r_index in range(0, 3):
                        checker: Checker = Checker(r_index, c_index, "white")
                        tile.add_checker(checker)

                    if r_index in range(5, 8):
                        checker: Checker = Checker(r_index, c_index, "red")
                        tile.add_checker(checker)

                row.append(tile)
            self.board.append(row)

    def set_next_turn(self) -> None:
        self.turn = (self.turn + 1) % 2

    def is_selected(self) -> bool:
        return self.selected != (None, None)

    def set_selected(self, row: int, col: int) -> bool:
        if self.board[row][col].has_checker():
            checker = self.board[row][col].checker

            if checker.color == self.players[self.turn]:
                self.selected = (row, col)
                return True
            else:
                self.selected = (None, None)

        return False

    def move_checker(self, row: int, col: int) -> None:
        assert self.is_selected()

        cur_row: Union[None, int] = self.selected[0]
        cur_col: Union[None, int] = self.selected[1]

        checker = self.board[cur_row][cur_col].checker
        if checker.is_queen:
            max_valid_moves = [(cur_row + i, cur_col + j) for i in [-1, 1] for j in [-1, 1]]
            max_valid_attacks = [(cur_row + i, cur_col + j) for i in [-2, 2] for j in [-2, 2]]
        else:
            if self.turn == 0:
                max_valid_moves = [(cur_row + i, cur_col + j) for i in [-1] for j in [-1, 1]]
                max_valid_attacks = [(cur_row + i, cur_col + j) for i in [-2] for j in [-2, 2]]
            else:
                max_valid_moves = [(cur_row + i, cur_col + j) for i in [1] for j in [-1, 1]]
                max_valid_attacks = [(cur_row + i, cur_col + j) for i in [2] for j in [-2, 2]]

        max_valid_moves = [pos for pos in max_valid_moves if pos[0] in range(8) and pos[1] in range(8)]
        max_valid_attacks = [pos for pos in max_valid_attacks if pos[0] in range(8) and pos[1] in range(8)]

        max_valid_moves = [pos for pos in max_valid_moves if not self.board[pos[0]][pos[1]].has_checker()]
        max_valid_attacks = [pos for pos in max_valid_attacks if not self.board[pos[0]][pos[1]].has_checker()]

        new_valid: List = []
        for pos in max_valid_attacks:
            tile: Tile = self.board[int((cur_row + pos[0]) // 2)][int((cur_col + pos[1]) // 2)]
            if tile.has_checker() and tile.checker.color != checker.color:
                new_valid.append(pos)

        max_valid_attacks = new_valid

        if (row, col) in max_valid_moves:
            moved_piece: Union[int, Checker] = self.board[cur_row][cur_col].remove_checker()
            moved_piece.row = row
            moved_piece.col = col

            if moved_piece.color == self.players[0]:
                if moved_piece.row == 0:
                    moved_piece.is_queen = True
            elif moved_piece.color == self.players[1]:
                if moved_piece.row == 7:
                    moved_piece.is_queen = True

            self.board[row][col].add_checker(moved_piece)
            self.set_next_turn()
        elif (row, col) in max_valid_attacks:
            moved_piece: Union[int, Checker] = self.board[cur_row][cur_col].remove_checker()
            moved_piece.row = row
            moved_piece.col = col

            if moved_piece.color == self.players[0]:
                if moved_piece.row == 0:
                    moved_piece.is_queen = True
            elif moved_piece.color == self.players[1]:
                if moved_piece.row == 7:
                    moved_piece.is_queen = True

            self.board[row][col].add_checker(moved_piece)
            self.board[int((row + cur_row) // 2)][int((col + cur_col) // 2)].remove_checker()

        self.selected = (None, None)        
