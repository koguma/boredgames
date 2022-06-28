from typing import Union
from fastapi import FastAPI, status, HTTPException
from create import create
from game import Game


games = ["connect-4"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create/", status_code=status.HTTP_201_CREATED)
def create_game(game: Game):
    if game.type not in games:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid game type")
    new_game = create()
    return new_game

