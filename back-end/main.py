from fastapi import FastAPI, status, HTTPException
from game import Room, Sentinel

sentinel = Sentinel()

app = FastAPI()

@app.get("/")
def read_root():
    return "Stop right there"

@app.post("/create/", status_code=status.HTTP_201_CREATED)
def create_room(room: Room):
    new_room = sentinel.create(room)
    
    if not new_room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating the room")
    
    return new_room