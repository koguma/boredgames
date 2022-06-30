from pydantic import BaseModel
from typing import Union
from fastapi import  WebSocket

class Room(BaseModel):
    type: str
    room_id: str
    is_private: bool

class Game:
    def __init__(self, room_id: str, is_private: bool) -> None:
        self.connections = {}
        self.room_id = room_id
        self.MAX_PLAYERS = 1
        self.is_private = is_private

    def add_player(self, websocket: WebSocket) -> bool:
        flag = False

        if len(self.connections) < self.MAX_PLAYERS:
            self.connections[websocket] = len(self.connections) + 1
            flag = True

        return flag

    def disconnect_all(self) -> None:
        self.connections = {}
    
    def disconnect(self, websocket: WebSocket) -> None:
        self.connections.pop(websocket)
        
    def get_player(self, websocket: WebSocket) -> int:
        return self.connections[websocket]
    
    def is_ready(self) -> bool:
        return len(self.connections) == self.MAX_PLAYERS

    async def broadcast(self, mesage: dict):
        for websocket in self.connections:
            await websocket.send_json(mesage)

class Connect_4(Game):
    def __init__(self, room_id : str, is_private: bool) -> None:
        super().__init__(room_id, is_private)
        self.MAX_PLAYERS = 2
        self.board = [[0]*6 for _ in range(7)]
        self.current_player = 1
        self.remaining_space = 6*7

    def make_move(self, player: int, coords: tuple) -> int:
        if player != self.current_player:
            return -1
        self.board[coords[0]][coords[1]] = self.current_player
        self.remaining_space -= 1
        
        if self.is_game_over(): return self.current_player
        if self.remaining_space == 0: return 3

        self.current_player = 1 if self.current_player == 2 else 2

        return 0
    
    def is_game_over(self) -> bool:  
        for i, column in enumerate(self.board):
            square = column[3]
            if square == self.current_player and self.is_same_vertically(i):
                return True

        for i, square in enumerate(self.board[3]):
            if square == self.current_player and (self.is_same_horizontally(i) or self.is_same_diagonally(i)):
                return True
        
        return False

    def is_same_diagonally(self, row: int) -> bool:
        count = 1 + self.diagonal_forward_count(4, row+1, True) + self.diagonal_forward_count(2, row-1, False)
        if count < 4: 
            count = 1 + self.diagonal_backward_count(2, row+1, True) + self.diagonal_backward_count(4, row-1, False)
        return True if count >= 4 else False

    def is_same_vertically(self, column: int) -> bool:
        count = 1 + self.vertical_count(column, 4, True) + self.vertical_count(column, 2, False)
        
        return True if count >= 4 else False

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
        self.games = ["connect-4"]
        self.rooms = {game_type: [] for game_type in self.games}
    
    def create_room(self, game: Room) -> Union[str,int]:
        # guard statements
        if game.type not in self.games: return 1
        if len(game.room_id) == 0: return 2
        if any(game.room_id == room.room_id for room in self.rooms[game.type]): return 3

        if game.type == "connect-4":
            new_game = Connect_4(game.room_id, game.is_private)
        self.rooms[game.type].append(new_game)
        
        return f"/rooms/{game.type}/{new_game.room_id}"

    def remove_room(self, game_type: str, room: Game) -> int:
        if game_type not in self.games: return 1
        room.disconnect_all()
        self.rooms[game_type].remove(room)

    def get_all_rooms(self) -> dict:
        return {game_type: [(i,game.room_id) for i, game in enumerate(self.rooms[game_type])] for game_type in self.rooms}
    
    def join_room(self, websocket: WebSocket, game_type: str, room_id: str) -> Union[Game, int]:
        if game_type not in self.rooms: return 1
        
        room = next((game for game in self.rooms[game_type] if game.room_id == room_id), None)
        
        if not room: return 2
        if not room.add_player(websocket): return 3
        
        return room