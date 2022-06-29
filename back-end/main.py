from fastapi import FastAPI, WebSocketDisconnect, status, HTTPException, WebSocket
import websockets
from game import Room, Sentinel
from fastapi.middleware.cors import CORSMiddleware

sentinel = Sentinel()

origins = [
    "http://127.0.0.1:3000",
    "http://127.0.0.1"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create/", status_code=status.HTTP_201_CREATED)
def create_room(room: Room):
    new_room = sentinel.create(room)
    
    if new_room == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid game-type")
    elif new_room == 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room ID must be >= 1 character")
    elif new_room == 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room ID already exists")
    return new_room

@app.get("/rooms/{type}")
def get_rooms(type: str):
    result = sentinel.list_rooms(type)
    if result == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid game-type")

    return result

@app.websocket("/ws/{type}/{room_id}")
async def join_room(websocket: WebSocket, type: str, room_id: int, player_number : int):
    game = sentinel.find_room(type, room_id)
    await websocket.accept()

    if game == -1:
        await websocket.close(1001, "Room does not exist")

    if not game.add_player(websocket):
        await websocket.close(1002, "Room is full")

    play = True
    try:
        while play:
            if len(game.players) == 2:
                if game.next_player_number == player_number:
                    coord = await websocket.receive_text()
                    coordinates = coord.split(",").strip("()")
                    winner = game.make_move(player_number, tuple(int(coordinates[0], int(coordinates[1]))))
                    if winner == -1:
                        await game.broadcast(f"{player_number} {coord}")
                    else:
                        await game.broadcast(f"{player_number} won")
                        await game.remove_player(websocket)
                        sentinel.remove_room(game)
                        play = False

    except WebSocketDisconnect:
        await game.remove_player(websocket)
        await game.broadcast(f"{player_number} disconnected")
        sentinel.remove_room(game)

    await websocket.close(1000)