from game import MultiPlayerBoardGame
from typing import Tuple

class Connect4(MultiPlayerBoardGame):
    def __init__(self, room_id : str) -> None:
        super().__init__(room_id, 2, 6, 7)

    def make_move(self, player: int, column: int) -> Tuple[int, Tuple[int,int]]:
        if not self.started:
            raise RuntimeError("The game has not started yet")

        if player != self.current_player:
            raise RuntimeError("It is not your turn yet")
        
        for i in reversed(range(len(self.dimensions["row"]))):
            if self.board[column][i] == 0:
                self.board[column][i] = self.current_player
                coords = (column, i)
                break
        else:
            raise RuntimeError("The selected column is full")
        
        winner = 0

        if self.is_vertical_win(coords) or self.is_horizontal_win(coords) or self.is_diagonal_win(coords):
            winner = self.current_player
            self.is_over = True
        elif self.board_is_full():
            winner = 3
            self.is_over = True
        
        self.next_turn()

        return (winner, coords)

    def next_turn(self) -> None:
        self.current_player = 1 if self.current_player == 2 else 2

    def board_is_full(self) -> bool:
        return all(self.board[i][0] for i in range(self.dimensions["col"]))

    def is_diagonal_win(self, coords: Tuple[int, int]) -> bool:
        x,y = coords
        count = 1 + self.diagonal_forward_count(x+1, y+1, True) + self.diagonal_forward_count(x-1, y-1, False)
        if count >= 4: return True

        count = 1 + self.diagonal_backward_count(x-1, y+1, True) + self.diagonal_backward_count(x+1, y-1, False)
        return count >= 4

    def is_vertical_win(self, coords: Tuple[int, int]) -> bool:
        x,y = coords
        count = 1 + self.vertical_count(x, y+1, True) + self.vertical_count(x, y-1, False)
        return count >= 4

    def is_horizontal_win(self, coords: Tuple[int, int]) -> bool:
        x,y = coords
        count = 1 + self.horizontal_count(x-1, y, True) + self.horizontal_count(x+1, y, False)
        return count >= 4

    def diagonal_backward_count(self, x: int, y: int, up: bool) -> int:
        if up:
            if x < 0 or y > 5 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.diagonal_backward_count(x-1,y+1,up)
        else:
            if x > 6 or y < 0 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.diagonal_backward_count(x+1,y-1,up)

    def diagonal_backward_count(self, x: int, y: int, up: bool) -> int:
        if up:
            if x < 0 or y > 5 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.diagonal_backward_count(x-1,y+1,up)
        else:
            if x > 6 or y < 0 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.diagonal_backward_count(x+1,y-1,up)

    def diagonal_forward_count(self, x: int, y: int, up: bool) -> int:
        if up:
            if x > 6 or y > 5 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.diagonal_forward_count(x+1,y+1,up)
        else:
            if x < 0 or y < 0 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.diagonal_forward_count(x-1,y-1,up)

    def vertical_count(self, x: int, y: int, up: bool) -> int:
        if up:
            if y > 5 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.vertical_count(x, y+1, up)
        else:
            if y < 0 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.vertical_count(x, y-1, up)

    def horizontal_count(self, x: int, y: int, left: bool) -> int:
        if left:
            if x < 0 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.horizontal_count(x-1, y, left)
        else:
            if x > 6 or self.board[x][y] != self.current_player:
                return 0
            else:
                return 1 + self.horizontal_count(x+1, y, left)