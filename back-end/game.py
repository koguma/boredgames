import json
from typing import Dict, Tuple
from fastapi import  WebSocket
from random import shuffle, choice

class Game:
    def __init__(self, room_id: str, num_of_players: int) -> None:
        self.connections = {}
        self.room_id = room_id
        self.started = False
        self.unused_player_numbers = [i+1 for i in range(num_of_players)]
        shuffle(self.unused_player_numbers)

    def join(self, websocket: WebSocket) -> int:
        player = 0
        
        if not self.started:
            player = self.connections[websocket] = self.unused_player_numbers.pop()
        
            if len(self.unused_player_numbers) == 0:
                self.started = True
        
        return player

    async def send(self, websocket: WebSocket, message: dict) -> None:
        await websocket.send_json(message)

    # async def receive(self, websocket: WebSocket) -> Dict[str, object]:
    #     await websocket.receive_json()

    async def broadcast(self, message: Dict[str, object]) -> None:
        for websocket in self.connections:
            await self.send(websocket, message)

    def remove(self, websocket: WebSocket, player: int) -> None:
        self.unused_player_numbers.append(player) # add the disconnected player back to the pool
        self.connections.pop(websocket)

    async def exchange_names(self, player: int, nickname: str) -> None:
        for websocket in self.connections:
            if self.connections[websocket] != player:
                await self.send(websocket, {
                    "event": "started",
                    "opponent": nickname
                })

class Connect_4(Game):
    def __init__(self, room_id : str) -> None:
        super().__init__(room_id, 2)
        self.board = [[0]*6 for _ in range(7)]
        self.current_player = 1
        self.vote_reset = set()

    def reset_board(self, player: int) -> bool:
        self.vote_reset.add(player)
        if self.vote_reset == 2:
            self.board = [[0]*6 for _ in range(7)]
            self.current_player = choice([1,2])
            self.vote_reset = set()
            return True
        return False

    def make_move(self, player: int, column: int) -> Tuple[int, Tuple[int,int]]:
        winner = 0
        
        if not self.started:
            raise RuntimeError("The game has not started yet")

        if player != self.current_player:
            raise RuntimeError("It is not your turn yet")
        
        for i in reversed(range(6)):
            if self.board[column][i] == 0:
                self.board[column][i] = self.current_player
                coords = (column, i)
                break
        else:
            raise RuntimeError("The selected column is full")
        
        
        if self.is_vertical_win(coords) or self.is_horizontal_win(coords) or self.is_diagonal_win(coords):
            winner = self.current_player
        elif self.board_is_full():
            winner = 3
        
        self.next_turn()

        return (winner, coords)

    def next_turn(self) -> None:
        self.current_player = 1 if self.current_player == 2 else 2

    def board_is_full(self) -> bool:
        return all(self.board[i][0] for i in range(7))

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
