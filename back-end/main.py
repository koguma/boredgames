from fastapi import FastAPI, WebSocketDisconnect, status, HTTPException, WebSocket
from game import Room, Sentinel
from fastapi.middleware.cors import CORSMiddleware
import asyncio

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
    new_room = sentinel.create_room(room)
    
    if new_room == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid game-type")
    elif new_room == 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room ID must be >= 1 character")
    elif new_room == 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room already exists")

    return new_room

# @app.get("/rooms/{type}")
# def list_rooms(type: str):
#     result = sentinel.list_rooms(type)
    
#     if result == 1:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid game-type")
    
#     return result

@app.websocket("/ws/{game_type}/{room_id}")
async def join_room(websocket: WebSocket, game_type: str, room_id: str):
    await websocket.accept()
    game = sentinel.join_room(websocket, game_type, room_id)
    
    if game == 1:
        await websocket.close(status.WS_1003_UNSUPPORTED_DATA, "Invalid game-type")
    elif game == 2:
        await websocket.close(status.WS_1003_UNSUPPORTED_DATA, "Room does not exist")
    elif game == 3:
        await websocket.close(status.WS_1013_TRY_AGAIN_LATER, "Room is full")
    else:
        player = game.get_player(websocket)
        await websocket.send_json({"player": player})
        try:
            while True:
                if game.is_ready() and game.current_player == player:
                    coord = await websocket.receive_text()
                    coords = tuple(map(int,coord.split(",")))
                    winner = game.make_move(player, coords)
                    if winner == 0:
                        await game.broadcast({
                            "x": coords[0],
                            "y": coords[1],
                            "player": player
                        })
                    elif winner == 3:
                        await game.broadcast({"message": "draw"})
                        break
                    else:
                        await game.broadcast({"message": f"{player} won"})
                        break
                else:
                    await asyncio.sleep(1)
        except WebSocketDisconnect:
            game.disconnect(websocket)
            await game.broadcast({"message": f"{player} disconnected"})

        sentinel.remove_room(game_type,game)