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
        self.board = [[0]*6 for _ in range(7)]
        return self.room_id
        
    def make_move(self, player_id: int, coordinate: tuple) -> bool:
        self.board[coordinate[0], coordinate[1]] = player_id
        continue_game = self.calculate_win()
        return continue_game

    def calculate_win(self) -> bool:
        pass
    



class Sentinel:
    def __init__(self) -> None:
        self.games = {game_type: [] for game_type in games}
    
    def create(self, game: Room) -> Union[str,bool]:
        is_success = False
        url = "/rooms/"

        if game.type == "connect-4" and game.room_id not in self.games["connect-4"]:
            new_game = Connect_4(game.room_id)
            url += new_game.room_id
            is_success = True
        
        return url if is_success else False