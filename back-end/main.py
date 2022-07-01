from fastapi import FastAPI, WebSocketDisconnect, status, HTTPException, WebSocket
from game import Game, Connect_4
from typing import Union
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio

class Room(BaseModel):
    type: str
    room_id: str
    is_private: bool

class Sentinel:
    def __init__(self) -> None:
        self.games = ["connect-4"]
        self.public_rooms = {game_type: [] for game_type in self.games}
        self.private_rooms = {game_type: [] for game_type in self.games}
    
    def get_all_rooms(self) -> dict:
        rooms = {}

        rooms["public"] = [(i, room.room_id) for game_type in self.public_rooms for i, room in enumerate(self.public_rooms[game_type])]
        rooms["private"] = [(i, room.room_id) for game_type in self.public_rooms for i, room in enumerate(self.public_rooms[game_type])]

        return rooms

    def get_room(self, game_type: str, room_id: str, public: bool) -> Union[Game, int]:
        if game_type not in self.games: return 1


        if public:
            chosen_room = next((room for room in self.public_rooms[game_type] if not room.started), None)
        else:
            chosen_room = next((room for room in self.private_rooms[game_type] if room.room_id == room_id), None)
            if chosen_room is not None and chosen_room.started: return 2
        
        if chosen_room is None:
            chosen_room = self.create_room(game_type, room_id, public)

        return chosen_room

    def create_room(self, game_type: str, room_id: str, public: bool, ) -> Game:

        room = Connect_4(room_id)
        
        if public:
            self.public_rooms[game_type].append(room)
        else:
            self.private_rooms[game_type].append(room)
        
        return room

    def remove_room(self, game_type: str, room: Game, public: bool) -> None:
        if public:
            self.public_rooms[game_type].remove(room)
        else:
            self.private_rooms[game_type].remove(room)

sentinel = Sentinel()

origins = [
    "http://localhost:3000",
    "http://localhost"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{game_type}")
async def join_room(websocket: WebSocket, game_type: str, nickname: str, room_id: str = ""):
    await websocket.accept()

    public = room_id == ""
    game = sentinel.get_room(game_type, room_id, public)
    
    if game == 1:
        await websocket.close(status.WS_1008_POLICY_VIOLATION, "Invalid game-type")
    elif game == 2:
        await websocket.close(status.WS_1013_TRY_AGAIN_LATER, "Room is full")
    else:
        exchanged = False
        player = game.join(websocket)
        await game.send_direct_message(websocket, {"you": player})
        try:
            while True:
                if game.started:
                    if not exchanged:
                       await game.exchange_names(player, nickname)
                       exchanged = True
                    
                    coord = await game.recieve_text(websocket)
                    if game.current_player == player:
                        await asyncio.sleep(1)
                        x,y = map(int,coord.split(","))
                        winner = game.make_move(player, x, y)
                        if winner == 0:
                            await game.broadcast({
                                "x": x,
                                "y": y,
                                "player": player
                            })
                        elif winner == 1 or winner == 2:
                            await game.broadcast({"message": f"{player} won"})
                        else:
                            await game.broadcast({"message": "draw"})
                await asyncio.sleep(1)

        except WebSocketDisconnect:
            game.remove_connection(websocket)
            await game.broadcast({"message": f"{player} disconnected"})
            if len(game.connections) == 0:
                sentinel.remove_room(game_type, game, public)