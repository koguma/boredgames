from pydantic import BaseModel
from typing import Union
from fastapi import  WebSocket, status
import websockets

games = ["connect-4"]

class Room(BaseModel):
    type: str
    room_id: str
    is_private: bool

class Game:
    def __init__(self, room_id: str, is_private: bool) -> None:
        self.players : list[WebSocket] = []
        self.room_id = room_id
        self.MAX_PLAYERS = 1
        self.private = is_private
    
    def is_private(self) -> bool:
        return self.private
    
    def is_ready(self) -> bool:
        return len(self.players) == 2

    async def add_player(self, player: WebSocket) -> bool:
        player_number = -1
        await player.accept()
        
        if (len(self.players) < self.MAX_PLAYERS):
            self.players.append(player)
            player_number = len(self.players)
        else:
            await player.close(status.WS_1014_BAD_GATEWAY, "Room is full")

        return player_number

    async def broadcast(self, message: str) -> None:
        for player in self.players:
            await player.send_text(message)

COLUMNS_CONNECT_4 = 7
ROWS_CONNECT_4 = 6

class Connect_4(Game):
    def __init__(self, room_id : str, is_private: bool) -> None:
        super().__init__(room_id, is_private)
        self.MAX_PLAYERS = 2
        self.board = [[0]*ROWS_CONNECT_4 for _ in range(COLUMNS_CONNECT_4)] # column first then the row
        self.current_player = 1
        
    def make_move(self, coordinate: tuple) -> int:
        self.board[coordinate[0]][coordinate[1]] = self.current_player
        if self.calculate_all_wins(): return self.current_player
        self.next_turn()
        return 0

    def next_turn(self):
        if self.current_player == 1:
            self.current_player = 2
        elif self.current_player == 2:
            self.current_player = 1

    def calculate_all_wins(self) -> int:
        won = self.calculate_vertical_win()
        if not won:
            won = self.calculate_horizontal_and_diagonal_win()
        return won
    
    def calculate_vertical_win(self) -> bool:  
        for i, column in enumerate(self.board):
            square = column[3]
            if square == self.current_player and self.is_same_vertically(i):
                return True
        return False

    def calculate_horizontal_and_diagonal_win(self) -> bool:
        for i, square in enumerate(self.board[3]):
            if square == self.current_player and (self.is_same_horizontally(i) or self.is_same_forward_diagonally(i) or self.is_same_backward_diagonally(i)):
                return True
        return False

    def is_same_forward_diagonally(self, row: int) -> bool:
        count = 1
        count += self.diagonal_forward_count(4, row+1, True)
        count += self.diagonal_forward_count(2, row-1, False)
        return True if count >= 4 else False

    def is_same_backward_diagonally(self, row: int) -> bool:
        count = 1
        count += self.diagonal_backward_count(2, row+1, True)
        count += self.diagonal_backward_count(4, row-1, False)
        return True if count >= 4 else False

    # \ <= diagonal check like this
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

    # / <= diagonal check like this
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

    def is_same_vertically(self, column: int) -> bool:
        count = 1
        count += self.vertical_count(column, 4, True)
        count += self.vertical_count(column, 2, False)
        
        return True if count >= 4 else False

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

    def is_same_horizontally(self, row: int) -> bool:
        count = 1
        count += self.horizontal_count(2, row, True)
        count += self.horizontal_count(4, row, False)

        return True if count >= 4 else False

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

class Sentinel:
    def __init__(self) -> None:
        self.rooms = {game_type: [] for game_type in games}
    
    def create(self, game: Room) -> Union[str,int]:
        # guard statements
        if game.type != "connect-4": return 1
        if len(game.room_id) == 0: return 2
        for room in self.rooms["connect-4"]:
            if game.room_id == room.room_id: return 3

        new_game = Connect_4(game.room_id, game.is_private)
        self.rooms["connect-4"].append(new_game)
        
        return "/rooms/connect-4/" + new_game.room_id

    def list_rooms(self, game_type: str) -> Union[list[str], int]:
        return 1 if game_type not in self.rooms else [game.room_id for game in self.rooms[game_type]]
    
    def find_room(self, game_type: str, room_id: str) -> Union[Connect_4, int]:
        if game_type in self.rooms:
            for room in self.rooms[game_type]:
                if room.room_id == room_id:
                    return room
        return -1

    def remove_room(self, room: Connect_4):
        self.rooms["connect-4"].remove(room)