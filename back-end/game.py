from curses import intrflush
from operator import indexOf
from tokenize import String
import xdrlib
from pydantic import BaseModel
from typing import Union

games = ["connect-4"]

class Room(BaseModel):
    type: str
    room_id: str
    creator: str

class Game:
    def __init__(self, room_id: str) -> None:
        self.players = []
        self.room_id = room_id
        self.MAX_PLAYERS = 1

    def add_player(self, player: str) -> bool:
        is_success = False
        
        if (len(self.players) <= self.MAX_PLAYERS):
            self.players.append(player)
            is_success = True

        return is_success

class Connect_4(Game):
    def __init__(self, room_id : str, creator: str) -> str:
        super(room_id)
        self.MAX_PLAYERS = 2
        self.add_player(creator)
        self.board = [[0]*7 for _ in range(6)] # column first then the row
        return self.room_id
        
    def make_move(self, player_id: int, coordinate: tuple) -> int:
        self.board[coordinate[0], coordinate[1]] = player_id
        continue_game = self.calculate_all_wins()
        return continue_game

    def calculate_all_wins(self) -> int:
        winner = self.calculate_vertical_win()
        if winner != -1: return winner

        return max(self.calculate_horizontal_and_diagonal_win(), winner)
    
    def calculate_vertical_win(self) -> int:  
        for i, column in enumerate(self.board):
            square = column[3]
            if square != 0 and self.is_same_vertically(i, square):
                return square
        return -1

    def calculate_horizontal_and_diagonal_win(self) -> int:

        for i, square in enumerate(self.board[3]):
            if square != 0:
                if self.is_same_horizontally(i, square): return square
                if self.is_same_forward_diagonally(i, square): return square
                if self.is_same_backward_diagonally(i, square): return square
        return -1

    def is_same_forward_diagonally(self, row: int, square: int) -> bool:
        count = 1
        count += self.diagonal_forward_count(4, row+1, square, True)
        count += self.diagonal_forward_count(2, row-1, square, True)
        return True if count >= 4 else False

    def is_same_backward_diagonally(self, row: int, square: int) -> bool:
        count = 1
        count += self.diagonal_backward_count(2, row+1, square, True)
        count += self.diagonal_backward_count(4, row-1, square, True)
        return True if count >= 4 else False

    # \ <= diagonal check like this
    def diagonal_backward_count(self, x: int, y: int, square: int, up: bool) -> int:
        if up:
            if x < 0 or y > 5 or self.board[x][y] != square:
                return 0
            else:
                return 1 + self.diagonal_backward_count(x-1,y+1,square,up)
        else:
            if x > 6 or y < 0 or self.board[x][y] != square:
                return 0
            else:
                return 1 + self.diagonal_backward_count(x+1,y-1,square,up)

    # / <= diagonal check like this
    def diagonal_forward_count(self, x: int, y: int, square: int, up: bool) -> int:
        if up:
            if x > 6 or y > 5 or self.board[x][y] != square:
                return 0
            else:
                return 1 + self.diagonal_forward_count(x+1,y+1,square,up)
        else:
            if x < 0 or y < 0 or self.board[x][y] != square:
                return 0
            else:
                return 1 + self.diagonal_forward_count(x-1,y-1,square,up)

    def is_same_vertically(self, column: int, square: int) -> bool:
        count = 1
        count += self.vertical_count(column, 4, square, True)
        count += self.vertical_count(column, 2, square, False)
        
        return True if count >= 4 else False

    def vertical_count(self, x: int, y: int, square: int, up: bool) -> int:
        if up:
            if y > 5 or self.grid[x][y] != square:
                return 0
            else:
                return 1 + self.vertical_count(x, y+1, square, up)
        else:
            if y < 0 or self.grid[x][y] != square:
                return 0
            else:
                return 1 + self.vertical_count(x, y-1, square, up)

    def is_same_horizontally(self, row: int, square: int) -> bool:
        count = 1
        count += self.horizontal_count(2, row, square, True)
        count += self.horizontal_count(4, row, square, False)

        return True if count >= 4 else False

    def horizontal_count(self, x: int, y: int, square: int, left: bool) -> int:
        if left:
            if x < 0 or self.grid[x][y] != square:
                return 0
            else:
                return 1 + self.horizontal_count(x-1, y, square, left)
        else:
            if x > 6 or self.grid[x][y] != square:
                return 0
            else:
                return 1 + self.horizontal_count(x+1, y, square, left)

class Sentinel:
    def __init__(self) -> None:
        self.rooms = {game_type: [] for game_type in games}
    
    def create(self, game: Room) -> Union[str,int]:
        # guard statements
        if game.type != "connect-4": return 1
        if len(game.room_id) == 0: return 2
        if game.room_id in self.rooms["connect-4"]: return 3

        new_game = Connect_4(game.room_id)
        url = "/rooms/connect-4/" + new_game.room_id
        self.rooms["connect-4"].append(new_game)
        
        return url

    def list_rooms(self, game_type: str) -> Union[list[str], int]:
        return 1 if game_type not in self.rooms else [game.room_id for game in self.rooms[game_type]]