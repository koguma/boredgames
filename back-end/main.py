from fastapi import FastAPI, status, HTTPException, WebSocket
from game import Room, Sentinel

sentinel = Sentinel()

app = FastAPI()

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