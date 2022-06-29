from curses import intrflush
from operator import indexOf
from tokenize import String
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

        winner = self.calculate_horizontal_and_diagonal_win()
        return winner
    
    def calculate_vertical_win(self) -> int:  
        for i, column in enumerate(self.board):
            square = column[3]
            if square != 0 and self.is_same_vertically(i, square):
                return square
        return -1


    def calculate_horizontal_and_diagonal_win(self) -> int:

        for i, square in enumerate(self.board[3]):
            if square != 0:
                if self.is_same_horizontally(i, square):
                    return square
                elif self.is_same_forward_diagonally(i, square):
                    return square
                elif self.is_same_backward_diagonally(i, square):
                    return square
        return -1

    def is_same_forward_diagonally(self, row: int, square: int) -> bool:
        count = 1
        return True

    def is_same_vertically(self, column: int, square: int) -> bool:
        count = 1
        count += self.vertical_count(column, 4, square, True)
        count += self.vertical_count(column, 2, square, False)
        
        return True if count >= 4 else False

    def vertical_count(self, column: int, y: int, square: int, up: bool) -> int:
        if up:
            if y > 5 or self.grid[column][y] != square:
                return 0
            else:
                return 1 + self.vertical_count(column, y+1, square, up)
        else:
            if y < 0 or self.grid[column][y] != square:
                return 0
            else:
                return 1 + self.vertical_count(column, y-1, square, up)

    def is_same_horizontally(self, row: int, square: int) -> bool:
        count = 1
        count += self.horizontal_count(row, 2, square, True)
        count += self.horizontal_count(row, 4, square, False)

        return True if count >= 4 else False

    def horizontal_count(self, row: int, x: int, square: int, left: bool) -> int:
        if left:
            if x < 0 or self.grid[x][row] != square:
                return 0
            else:
                return 1 + self.horizontal_count(row, x-1, square, left)
        else:
            if x > 6 or self.grid[x][row] != square:
                return 0
            else:
                return 1 + self.horizontal_count(row, x+1, square, left)

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