from enum import Enum

class GameState(Enum):
    ONGOING = 0
    WON = 1
    DRAW = -1

class TicTacToe:
    def __init__(self):
        self.clear_board()

    def __str__(self):
        string = f'{self.board[:3]}\n{self.board[3:6]}\n{self.board[6:]}'
        return string

    def clear_board(self):
        self.board = [0] * 9

    def get_gamestate(self):
        for i in range(3):
            if ((self.board[(i*3)+0] == self.board[(i*3)+1] == self.board[(i*3)+2] and
                self.board[(i*3)+0] + self.board[(i*3)+1] + self.board[(i*3)+2] > 0) or
                (self.board[i] == self.board[i+3] == self.board[i+6] and
                 self.board[i] + self.board[i+3] + self.board[i+6] > 0)):
                return GameState.WON
        if ((self.board[0] == self.board[4] == self.board[8] and
            self.board[0] + self.board[4] + self.board[8] > 0) or
           (self.board[2] == self.board[4] == self.board[6] and
            self.board[2] == self.board[4] == self.board[6] > 0)):
            return GameState.WON
        clear_tile_found = False
        for i in range(9):
            if self.board[i] == 0:
                clear_tile_found = True
                break
        if not clear_tile_found:
            return GameState.DRAW
        return GameState.ONGOING

    def get_inv_board(self):
        inv_board = [0]*9
        for i in range(9):
            if self.board[i] == 1:
                inv_board[i] = 2
            elif self.board[i] == 2:
                inv_board[i] = 1
        return inv_board

    @staticmethod
    def encode_board(board):
        encoded_board = 0
        for i, val in enumerate(board):
            encoded_board += (3**i * val)
        return encoded_board

    def play(self, player, tile_nr_or_row, col=None):
        if col is None:
            tile_nr = tile_nr_or_row
        else:
            row = tile_nr_or_row
            tile_nr = (row * 3) + col
        tile = self.board[tile_nr]
        if tile > 0:
            return False
        self.board[tile_nr] = player
        return True


