import asyncio
import json
from fastapi import FastAPI, WebSocketDisconnect, status, WebSocket
from game import Game, Player
from connect4 import Connect4
from checkers import Checkers, Piece
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Tuple
from math import floor, ceil
from random import choice, random

nicknames = ["John", "Ben", "Shiba", "Tom", "Tim", "Kong Ming", "Joe", "Spiderman", "Mona", "Link", "Sushiboy", "Squidquick", "Your penpal", "call me beep me", "Lebron James", "James Harden", "Curry", "Papa"]

current_index = -1
def get_next_name() -> str:
    global current_index
    current_index += 1
    try:
        return nicknames[current_index]
    except IndexError:
        current_index = -1
        return get_next_name()

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

                if chosen_room.started:
                    # make sure the chosen instance is not started yet
                    raise RuntimeError("Room ID is currently in use")
        
        except KeyError:
            # make sure it is a supported game
            raise RuntimeError("Invalid game-type")
        
        except AttributeError:
            pass

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

        try:
            player = await game.join(websocket, nickname) # join the game and be assigned a player number
            if player:
                total_online += 1 # increment total number of connections by 1
                
                # choose the correct method to handle each game
                if game_type == "connect-4":
                    await join_connect4(game, player)
                elif game_type == "checkers":
                    await join_checkers(game, player)

        except WebSocketDisconnect:
            # if the websocket connection drops, handle the cleanup

            total_online -= 1 # decrement total number of connections by 1
            game.remove(player) # remove the websocket/player from the game
            
            if game.dummy_plug.id:
                total_online -= 1

            # broadcast the disconnection
            await game.broadcast({
                "event": "disconnected",
                "message": f"{nickname} (opponent) disconnected"
            })
            
            # if all connections in the game is lost, remove the room
            if len(game.connections) == 0 or game.dummy_plug.id:
                try:
                    sentinel.remove_room(game_type, game, is_public)
                except RuntimeError:
                    pass

async def predict_next_connect4_move(game: Connect4):
    """
        used by the bot to generate the next connect 4 move. Implementation is bizzare but that's what makes it good
        NOTE: Actually stronger than me, I keep losing to it

        Args:
            game: the instance of connect 4 game the move should be calculated against
    """
    moves = {}
    me = game.dummy_plug.id
    opponent = 1 if game.dummy_plug.id == 2 else 2
    
    for col in range(game.dimensions["col"]):
        await asyncio.sleep(0.2)
        for i in reversed(range(game.dimensions["row"])):
            if game.board[col][i] == 0:
                rank = 0
                c = game.count_all_consecutive(me, col,i)
                
                rank = max(rank,c)
                
                if c < 3:
                    try:
                        n = game.count_all_consecutive(opponent, col,i+1)
                        if n >= 3:
                            rank = -100
                    except IndexError:
                        pass
                else:
                    await asyncio.sleep(0.4)
                    return col

                # prefer not putting on the corner if it is the bottom piece
                if game.board[3][i] == opponent and (col == 0 or col == 6) and i > 3 and rank != -100:
                    rank = -5

                n = game.count_all_consecutive(opponent, col,i)
                
                if n >= 3:
                    await asyncio.sleep(0.4)
                    return col
                
                if rank != -100:
                    rank = max(rank, n)

                if rank not in moves:
                    moves[rank] = []

                moves[rank].append(col)
                
                break

    lst = moves[max(moves.keys())]
    await asyncio.sleep(random()*1.2)

    if len(lst) == 1:
        return lst[0]
    else:
        return lst[choice([floor(len(lst)/2),ceil(len(lst)/2)])]

async def dummy_make_connect4_move(game: Connect4) -> None:
    """
        allow the dummy plug to make a connect 4 move

        Args:
            game: the instance of connect 4 game the move should be calculated against
    """
    next_move = await predict_next_connect4_move(game)

    # make a new move with the receieved event
    winner, coords = game.make_move(game.dummy_plug.id,next_move)
    
    # broadcast the move to all players
    await game.broadcast({
        "event": "move",
        "x": coords[0],
        "y": coords[1],
        "player": game.dummy_plug.id,
        "next": game.current_player
    })

    # if the winner is found, then broadcast that the game is over
    if game.is_over:
        await game.broadcast({
            "event": "end",
            "player": winner
        })

async def join_connect4(game: Connect4, player: Player):
    """
    Handle connect 4 games
    Args:
        game: current instance of the board game
        websocket: websocket client connecting to the endpoint
        room_id: room ID of the room the client wants to connect to
        game_type: type of game the client wants to connect to
    """
    global total_online

    while True:

        # recieve a new event from the websocket
        received = await player.connection.receive_json()
        try:
            if received["event"] == "force-start":
                if not game.started:
                    
                    # if game has not started yet, add the dummy plug
                    
                    ok = await game.join(None, get_next_name())
                    if ok:
                        total_online += 1
                        
                        if game.started and game.current_player == game.dummy_plug.id:
                            await dummy_make_connect4_move(game)

            elif received["event"] == "move" and not game.is_over:
                column = received["column"]
                
                # make a new move with the receieved event
                winner, coords = game.make_move(player.id, column)
                
                # broadcast the move to all players
                await game.broadcast({
                    "event": "move",
                    "x": coords[0],
                    "y": coords[1],
                    "player": player.id,
                    "next": game.current_player
                })

                # if the winner is found, then broadcast that the game is over
                if game.is_over:
                    await game.broadcast({
                        "event": "end",
                        "player": winner
                    })
                
                elif game.dummy_plug.id:
                    await dummy_make_connect4_move(game)

            elif received["event"] == "rematch" and game.is_over:
                success = game.reset_board(player.id) # cast their vote to reset the board

                # broadcast that the rematch is happening
                if success:
                    if game.dummy_plug.id:
                        await asyncio.sleep(random()*4)
                    await game.broadcast({
                        "event": "rematch",
                        "player": game.current_player
                    })

                    if game.current_player == game.dummy_plug.id:
                        await dummy_make_connect4_move(game)
                elif game.dummy_plug.id:
                    await asyncio.sleep(random()*4)
                    
                    # broadcast the disconnection
                    await game.broadcast({
                        "event": "disconnected",
                        "message": f"{game.dummy_plug.id} (opponent) disconnected"
                    })
            else:
                # message the client that the event is not valid 
                await game.send(player, {
                    "event": "error",
                    "message": "invalid event"
                })
        
        except RuntimeError as e:
            # relay any runtime error back to the client
            await game.send(player, {
                "event": "error",
                "message": str(e)
        })

async def predict_next_checkers_move(game: Checkers) -> Tuple[Tuple[int,int],Tuple[int,int]]:
    """
        used by the bot to generate the next checkers move. Implementation is bizzare but that's what makes it good
        NOTE: Actually stronger than me, I keep losing to it

        Args:
            game: the instance of connect 4 game the move should be calculated against
    """

    moves = {}

    if game.all_moves["moves_eat"][game.dummy_plug.id]:
        
        for starting_position in game.all_moves["moves_eat"][game.dummy_plug.id]:
            await asyncio.sleep(0.2)
            rank = 1

            piece = game.board[starting_position[0]][starting_position[1]]
            for move in game.all_moves["moves_eat"][game.dummy_plug.id][starting_position]:
                
                game.board[move["possible_move"][0]][move["possible_move"][1]] = piece
                game.board[starting_position[0]][starting_position[1]] = 0
                
                for x_displacement, y_displacement in Piece.moves_eat:
                    next_x, next_y = move["possible_move"][0]+x_displacement, move["possible_move"][1]+y_displacement
                    if game.is_valid_move(move["possible_move"], (next_x, next_y)):
                        rank += 10
                        break

                if rank == 1:
                    
                    for x_displacement, y_displacement in Piece.moves:
                        next_x, next_y = move["possible_move"][0]+x_displacement, move["possible_move"][1]+y_displacement
                        
                        try:
                            another_piece = game.board[next_x][next_y]
                            if another_piece.owner != game.dummy_plug.id:
                                for new_x, new_y in Piece.moves_eat:
                                    if game.is_valid_move((next_x, next_y), (next_x+new_x,next_y+new_y), assume_middle_piece=True):
                                        rank -= 100
                                        break

                        except (AttributeError, IndexError):
                            continue
                        
                        if rank != 1:
                            break

                if (starting_position[1] == 7 and piece.owner == 2) or (starting_position[1] == 0 and piece.owner == 1):
                    rank -= 100
                
                elif not piece.is_king and (move["possible_move"][1] == 7 and piece.owner == 1) or (move["possible_move"][1] == 0 and piece.owner == 2):
                    rank += 1
                elif piece.is_king and (move["possible_move"][1] == 7 and piece.owner == 1) or (move["possible_move"][1] == 0 and piece.owner == 2):
                    rank -= 100

                game.board[move["possible_move"][0]][move["possible_move"][1]] = 0
                game.board[starting_position[0]][starting_position[1]] = piece
                
                if rank not in moves:
                    moves[rank] = []
                
                moves[rank].append((starting_position, move["possible_move"]))
    
    else:
        for starting_position in game.all_moves["moves"][game.dummy_plug.id]:
            await asyncio.sleep(0.2)
            
            piece = game.board[starting_position[0]][starting_position[1]]
            
            for move in game.all_moves["moves"][game.dummy_plug.id][starting_position]:
                game.board[move["possible_move"][0]][move["possible_move"][1]] = piece
                game.board[starting_position[0]][starting_position[1]] = 0
                rank = 1

                found = False

                for x_displacement, y_displacement in Piece.moves:
                    next_x, next_y = move["possible_move"][0]+x_displacement, move["possible_move"][1]+y_displacement
                    for new_x, new_y in Piece.moves_eat:
                        if game.is_valid_move((next_x, next_y), (next_x+new_x,next_y+new_y), assume_middle_piece=True):
                            try:
                                another_piece = game.board[next_x][next_y]
                                if another_piece.owner != game.dummy_plug.id:
                                    rank -= 100
                                    found = True
                                    break
                                else:
                                    rank += 3
                            except (AttributeError, IndexError):
                                continue
                    if found:
                        break
                
                if (starting_position[1] == 7 and piece.owner == 2) or (starting_position[1] == 0 and piece.owner == 1):
                    rank -= 100
                elif not piece.is_king and (move["possible_move"][1] == 7 and piece.owner == 1) or (move["possible_move"][1] == 0 and piece.owner == 2):
                    rank += 1

                game.board[move["possible_move"][0]][move["possible_move"][1]] = 0
                game.board[starting_position[0]][starting_position[1]] = piece
                
                if rank not in moves:
                    moves[rank] = []

                moves[rank].append((starting_position, move["possible_move"]))
    
    await asyncio.sleep(random()*2)
    lst = moves[max(moves.keys())]
    return choice(lst)

async def dummy_make_checkers_move(game: Checkers) -> None:
    """
        allow the dummy plug to make a checkers move

        Args:
            game: the instance of connect 4 game the move should be calculated against
    """
    starting_position, next_position = await predict_next_checkers_move(game)

    #get the resulting move, and add a new JSON key event
    result, winner = game.make_move(game.dummy_plug.id, starting_position, next_position)
    result.update({"event": "move"})

    # broadcast the move to all players
    await game.broadcast(result)

    # check if game is won, then broadcast that the game is over
    if game.is_over:
        await game.broadcast({
            "event": "end",
            "player": winner
        })
    
    elif game.current_player == game.dummy_plug.id:
        await dummy_make_checkers_move(game)

async def join_checkers(game: Checkers, player: Player) -> None:
    """
    Handle checkers game

    Args:
        game: current instance of the board game
        websocket: websocket client connecting to the endpoint
        room_id: room ID of the room the client wants to connect to
        game_type: type of game the client wants to connect to
    """
    global total_online

    while True:

        # recieve a new event from the websocket
        received = await player.connection.receive_json()
        
        try:
            if received["event"] == "force-start":
                if not game.started:
                    
                    # if game has not started yet, add the dummy plug
                    
                    ok = await game.join(None, get_next_name())
                    if ok:
                        total_online += 1
                        
                        if game.started and game.current_player == game.dummy_plug.id:
                            await dummy_make_checkers_move(game)
            
            elif received["event"] == "move" and not game.is_over:
                
                #get the resulting move, and add a new JSON key event
                result, winner = game.make_move(player.id, tuple(received["current_position"]), tuple(received["next_position"]))
                result.update({"event": "move"})

                # broadcast the move to all players
                await game.broadcast(result)

                # check if game is won, then broadcast that the game is over
                if game.is_over:
                    await game.broadcast({
                        "event": "end",
                        "player": winner
                    })
                
                elif game.current_player == game.dummy_plug.id:
                    await dummy_make_checkers_move(game)

            elif received["event"] == "rematch" and game.is_over:
                success = game.reset_board(player.id) # cast their vote to reset the board

                # broadcast that the rematch is happening
                if success:
                    if game.dummy_plug.id:
                        await asyncio.sleep(random()*4)
                    await game.broadcast({
                        "event": "rematch",
                        "player": game.current_player
                    })

                    if game.current_player == game.dummy_plug.id:
                        await dummy_make_checkers_move(game)
                elif game.dummy_plug.id:
                    await asyncio.sleep(random()*4)
                    
                    # broadcast the disconnection
                    await game.broadcast({
                        "event": "disconnected",
                        "message": f"{game.dummy_plug.nickname} (opponent) disconnected"
                    })
            elif received["event"] == "help" and not game.is_over:
                result = game.get_possible_moves(player.id, tuple(received["current_position"]))
                await game.send(player, {
                    "event": "answer",
                    "moves": result
                })

            else:
                # message the client that the event is not valid 
                await game.send(player, {
                    "event": "error",
                    "message": "invalid event"
                })
        
        except RuntimeError as e:
            # relay any runtime error back to the client
            await game.send(player, {
                "event": "error",
                "message": str(e)
        })