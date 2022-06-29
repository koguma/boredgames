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

    
    def is_same_vertically(self, column, square) -> bool:
        count = 1
        y1 = 2
        y2 = 4

        up = True
        down = True
        while y1 >= 0 and y2 <= 5 and (down or up):
            if down:
                if grid[column][y1] == square:
                    count += 1
                else:
                    down = False
                y1 -= 1
            if up:
                if grid[column][y2] == square:
                    count += 1
                else:
                    up = False
                y2 += 1
        
        return True if count >= 4 else False

    def calculate_horizontal_and_diagonal_win(self) -> int:
        middle_column = self.board[3]

        for i, square in enumerate(middle_column):
            if square != 0 and self.is_same_horizontally(i, square):
                return square
                

        return -1

    def is_same_horizontally(self, row, square) -> bool:
        count = 1
        x1 = 2
        x2 = 4

        left = True
        right =  True
        while x1 >= 0 and x2 <= 6 and (left or right):
            if left:
                if self.grid[x1][row] == square:
                    count += 1
                else:
                    left = False
                x1 -= 1
            if right:
                if self.grid[x2][row] == square:
                    count += 1
                else:
                    right = False
                x2 += 1

        return True if count >= 4 else False

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