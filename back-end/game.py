from fastapi import  WebSocket
from random import choice

class Game:
    def __init__(self, room_id: str, num_of_players: int) -> None:
        self.connections = {}
        self.room_id = room_id
        self.started = False
        self.unused_player_numbers = [i+1 for i in range(num_of_players)]

    def join(self, websocket: WebSocket) -> int:
        player = 0
        
        if not self.started:
            player = self.connections[websocket] = choice(self.unused_player_numbers)
            self.unused_player_numbers.remove(player)
        
            if len(self.unused_player_numbers) == 0:
                self.started = True
        
        return player

    async def send_direct_message(self, websocket: WebSocket, json: dict) -> None:
        await websocket.send_json(json)

    async def recieve_text(self, websocket: WebSocket) -> str:
        return await websocket.receive_text()

    async def broadcast(self, message: dict) -> None:
        for websocket in self.connections:
            await websocket.send_json(message)

    def remove_connection(self, websocket: WebSocket) -> None:
        self.connections.pop(websocket)
    
    async def close(self) -> None:
        for websocket in self.connections:
            await websocket.close()

    async def exchange_names(self, player: int, nickname: str) -> None:
        for websocket in self.connections:
            if self.connections[websocket] != player:
                await websocket.send_json({"opponent": nickname})

class Connect_4(Game):
    def __init__(self, room_id : str) -> None:
        super().__init__(room_id, 2)
        self.board = [[0]*6 for _ in range(7)]
        self.current_player = 1
        self.remaining_space = 6*7

    def make_move(self, player: int, x: int, y: int) -> int:
        if player != self.current_player:
            return -1
        self.board[x][y] = self.current_player
        self.remaining_space -= 1
        
        if self.is_winning_move(): return self.current_player
        if self.remaining_space == 0: return 3

        self.current_player = 1 if self.current_player == 2 else 2

        return 0
    
    def is_winning_move(self) -> bool:  
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

    def is_same_horizontally(self, row: int) -> bool:
        count = 1 + self.horizontal_count(2, row, True) + self.horizontal_count(4, row, False)

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
