from pydantic import BaseModel
from typing import Union
from fastapi import  WebSocket

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
        self.is_private = is_private

    async def add_player(self, player: WebSocket) -> bool:
        is_success = False
        
        if (len(self.players) <= self.MAX_PLAYERS):
            self.players.append(player)
            is_success = True

        return is_success

    def get_player_number(self, player: WebSocket) -> int:
        return self.players.index(player) + 1

    def remove_player(self, player: WebSocket) -> None:
        self.players.remove(player)

    async def broadcast(self, message: str) -> None:
        for player in self.players:
            await player.send_text(message)

class Connect_4(Game):
    def __init__(self, room_id : str, is_private: bool) -> None:
        super().__init__(room_id, is_private)
        self.MAX_PLAYERS = 2
        self.board = [[0]*7 for _ in range(6)] # column first then the row
        self.next_player_number = 1
        
    def make_move(self, player_number: int, coordinate: tuple) -> int:
        self.board[coordinate[0], coordinate[1]] = player_number
        continue_game = self.calculate_all_wins()

        self.next_turn()
        return continue_game

    def next_turn(self):
        if self.next_player_number == 1:
            self.next_player_number = 2
        else:
            self.next_player_number = 1

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
        for room in self.rooms["connect-4"]:
            if game.room_id == room.room_id: return 3

        print(self.rooms["connect-4"], game.room_id)
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