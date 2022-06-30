from fastapi import FastAPI, WebSocketDisconnect, status, HTTPException, WebSocket
from game import Room, Sentinel
from fastapi.middleware.cors import CORSMiddleware

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
async def join_room(websocket: WebSocket, type: str, room_id: str):
    game = sentinel.find_room(type, room_id)
    if game == -1: return

    player_number = await game.add_player(websocket)
    await websocket.send_text(f"{player_number}")
    try:
        while True:
            if game.is_ready():
                print("hi")
                if game.next_player_number == player_number:
                    coord = await websocket.receive_text()
                    coordinates = coord.split(",").strip("()")
                    winner = game.make_move(player_number, tuple(int(coordinates[0], int(coordinates[1]))))
                    if winner == -1:
                        await game.broadcast(f"{player_number} {coord}")
                    else:
                        await game.broadcast(f"{player_number} won")
                        sentinel.remove_room(game)
                        return

    except WebSocketDisconnect:
        await game.broadcast(f"{player_number} disconnected")
        sentinel.remove_room(game)