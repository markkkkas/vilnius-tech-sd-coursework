from .tile import Tile
from .checker import Checker


class Game:
    def __init__(self):
        self.players = ['red', 'white']
        self.selected = (None, None)
        self.board = []
        self.turn = 0

        for r_index in range(8):
            row = []

            for c_index in range(8):
                tile = Tile(r_index, c_index, Tile.tile_colors[(r_index + c_index) % 2])

                if tile.color == Tile.tile_colors[1]:
                    if r_index in range(0, 3):
                        checker = Checker(r_index, c_index, "white")
                        tile.add_checker(checker)

                    if r_index in range(5, 8):
                        checker = Checker(r_index, c_index, "red")
                        tile.add_checker(checker)

                row.append(tile)
            self.board.append(row)

    def set_next_turn(self):
        self.turn = (self.turn + 1) % 2

    def is_selected(self):
        return self.selected != (None, None)

    def set_selected(self, row, col):
        if self.board[row][col].has_checker():
            piece = self.board[row][col].checker
            if piece.color == self.players[self.turn]:
                self.selected = (row, col)
                return True
            else:
                self.selected = (None, None)
        return False

    def move_checker(self, row, col):
        assert self.is_selected()
        cur_row = self.selected[0]
        cur_col = self.selected[1]
        piece = self.board[cur_row][cur_col].checker
        if piece.is_queen:
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

        new_valid = []
        for pos in max_valid_attacks:
            middle = self.board[int((cur_row + pos[0]) // 2)][int((cur_col + pos[1]) // 2)]
            if middle.has_checker() and middle.checker.color != piece.color:
                new_valid.append(pos)
        max_valid_attacks = new_valid

        if (row, col) in max_valid_moves:
            moved_piece = self.board[cur_row][cur_col].remove_checker()
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
            moved_piece = self.board[cur_row][cur_col].remove_checker()
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
