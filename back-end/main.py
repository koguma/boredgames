import json
from fastapi import FastAPI, WebSocketDisconnect, status, WebSocket
from game import Game
from connect4 import Connect4
from checkers import Checkers
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Tuple

class Sentinel:
    """
        Class used to create an object which provide central management for all rooms

        Attributes:
            games: list of all supported game types
            public_rooms: dictionary mapping all games to a list of all public Game instances
            private_rooms: dictionary mapping all games to a list of Game instances
    """

    games = ["connect-4", "checkers"]

    def __init__(self) -> None:
        """
        Constructor to instantiate an object of the class
        """

        # initialise public_rooms and private_rooms
        self.public_rooms = {game_type: [] for game_type in self.games}
        self.private_rooms = {game_type: [] for game_type in self.games}
    

    def get_all_rooms(self) -> Dict[str,List[Tuple[int,str]]]:
        """
        Get a view of all rooms that are currently being handled
        
        Returns:
            all rooms that are currently being managed
        """

        rooms = {}

        # cycle through all room ids in every room for every game type in public rooms
        rooms["public"] = [(i, room.room_id) for game_type in self.public_rooms for i, room in enumerate(self.public_rooms[game_type])]

        # cycle through all room ids in every room for every game type in public rooms
        rooms["private"] = [(i, room.room_id) for game_type in self.public_rooms for i, room in enumerate(self.public_rooms[game_type])]

        return rooms

    def get_room(self, game_type: str, room_id: str, is_public: bool) -> Game:
        """
        Get a room that follows a particular criteria which can currently be joined
        
        Args:
            game_type: type of game the room is for
            room_id: id of the room
            is_public: whether the room is a public or private

        Returns:
            Game instance that is currently joinable
        """ 

        try:
            if is_public:
                # search for the first public Game instance that has not started yet
                chosen_room = next((room for room in self.public_rooms[game_type] if not room.started), None)
            
            else:
                # search for the first private Game instance that matches the input room_id
                chosen_room = next((room for room in self.private_rooms[game_type] if room.room_id == room_id), None)

                assert chosen_room is None or not chosen_room.started
        
        except KeyError:
            # make sure it is a supported game
            raise RuntimeError("Invalid game-type")

        except AssertionError:
            # make sure the chosen instance is not started yet
            raise RuntimeError("Room ID is currently in use")

        # create a new room if no available room found
        if chosen_room is None:
            chosen_room = self.create_room(game_type, room_id, is_public)

        return chosen_room

    def create_room(self, game_type: str, room_id: str, is_public: bool) -> Game:
        """
        Create a new room. Assumes that the game_type is valid as it is only called by get_room function
        
        Args:
            game_type: type of game the room is for
            room_id: id of the room
            is_public: whether the room is a public or private

        Returns:
            new Game instance
        """

        # create a new room with appropriate class
        if game_type == "connect-4":
            room = Connect4(room_id)
        elif game_type == "checkers":
            room = Checkers(room_id)
        
        # add it to the correct dictionary depending on the chosen access permission
        if is_public:
            self.public_rooms[game_type].append(room)
        else:
            self.private_rooms[game_type].append(room)
        
        return room

    def remove_room(self, game_type: str, room: Game, is_public: bool) -> None:
        """
        Remove a room
        
        Args:
            game_type: type of game the room is for
            room: room to be deleted
            is_public: whether the room is a public or private
        """

        # remove it from the correct dictionary depending on the chosen access permission
        try:
            if is_public:
                self.public_rooms[game_type].remove(room)
            else:
                self.private_rooms[game_type].remove(room)
        except KeyError:
            raise RuntimeError("Room does not exist")


# instantiate sentinel and app
sentinel = Sentinel()
app = FastAPI()

# CORS whitelisting
origins = [
    "http://localhost:3000",
    "http://localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

total_online = 0 # store current total of connections

@app.get("/statistics")
async def get_statistics() -> str:
    """
    Handle GET request to /statistics end-point to show current statistics of the app

    Returns:
        current statistics as a JSON string
    """
    
    global total_online
    return json.dumps({"total": total_online})

@app.websocket("/ws/{game_type}")
async def join_room(websocket: WebSocket, game_type: str, nickname: str, room_id: str = "") -> None:
    """
    Handle ws request to /ws/ end-points to allow connection to games

    Args:
        websocket: websocket client connecting to the endpoint
        game_type: type of game the client wants to connect to
        nickname: nickname the websocket client is using
        room_id: room ID of the room the client wants to connect to
    """

    global total_online
    is_public = room_id == "" # if room_id is empty, then it is a public game

    await websocket.accept() # acccept the incoming websocket connection

    try:
        game = sentinel.get_room(game_type, room_id, is_public) # get an available game from sentinel
    
    except RuntimeError as e:
        # if any runtime error raised, close the connection
        await websocket.close(status.WS_1006_ABNORMAL_CLOSURE, e)
    
    else:
        player = game.join(websocket) # join the game and be assigned a player number

        # notify the client of their player number
        await game.send(websocket, {
            "event": "connected",
            "you": player
        })

        try:
            total_online += 1 # increment total number of connections by 1

            # choose the correct method to handle each game
            if game_type == "connect-4":
                await join_connect4(game, websocket, nickname, player)
            elif game_type == "checkers":
                await join_checkers(game, websocket, nickname, player)
        
        except WebSocketDisconnect:
            # if the websocket connection drops, handle the cleanup

            total_online -= 1 # decrement total number of connections by 1
            game.remove(websocket, player) # remove the websocket/player from the game
            
            # broadcast the disconnection
            await game.broadcast({
                "event": "disconnected",
                "message": f"{nickname} (opponent) disconnected"
            })
            
            # if all connections in the game is lost, remove the room
            if len(game.connections) == 0:
                try:
                    sentinel.remove_room(game_type, game, is_public)
                except RuntimeError:
                    pass

async def join_connect4(game: Connect4, websocket: WebSocket, nickname: str, player: int):
    """
    Handle connect4 games

    Args:
        game: current game of connect4
        websocket: websocket client connecting to the endpoint
        nickname: nickname the websocket client is using
        room_id: room ID of the room the client wants to connect to
    """

    exchanged = False # store whether the nickname exchanged happened or not

    while True:

        # exchange names if not done so and the game has already started
        if not exchanged and game.started:
            await game.exchange_names(websocket, nickname)
            exchanged = True

        # recieve a new event from the websocket
        received = await websocket.receive_json()

        if received["event"] == "move" and not game.is_over:
            try:

                column = received["column"]
                winner, coords = game.make_move(player, column) # make a new move with the receieved event
                
                # broadcast the move to all players
                await game.broadcast({
                    "event": "move",
                    "x": coords[0],
                    "y": coords[1],
                    "player": player,
                    "next": game.current_player
                })

                # if the winner is found, then broadcast that the game is over
                if winner:
                    await game.broadcast({
                        "event": "end",
                        "player": winner
                    })

            except RuntimeError as e:
                # relay any runtime error back to the client
                await game.send(websocket, {
                    "event": "error",
                    "message": str(e)
                })
        
        elif received["event"] == "rematch" and game.is_over:
            success = game.reset_board(player) # cast their vote to reset the board

            # broadcast that the rematch is happening
            if success:
                await game.broadcast({
                    "event": "rematch",
                    "player": game.current_player
                })
        else:
            # message the client that the event is not valid 
            await game.send(websocket, {
                "event": "error",
                "message": "invalid event"
            })

async def join_checkers(game: Game, websocket: WebSocket, nickname: str, player: int):
    """
    Handle connect4 games

    Args:
        game: current game of connect4
        websocket: websocket client connecting to the endpoint
        nickname: nickname the websocket client is using
        room_id: room ID of the room the client wants to connect to
    """

    pass