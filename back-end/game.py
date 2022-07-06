from typing import Dict
from fastapi import WebSocket
from random import shuffle, choice

class Game:
    """
    The base class used to create all games

    Attributes:
        connections: dictionary that maps connected websockets to their corresponding player number
        room_id: ID of the created instance
        started: whether the game has started or not
        unused_player_numbers: stores the player numbers that are currently assignable
        used_player_numbers: stores the player numbers that are already assigned
    """

    def __init__(self, room_id: str, num_of_players: int) -> None:
        """
        Constructor to instantiate an object of the class

        Args:
            room_id: id of the room being created
            num_of_players: number of players the game is created for
        """

        self.connections = {}
        self.room_id = room_id 
        self.started = False
        self.unused_player_numbers = [i+1 for i in range(num_of_players)]
        self.used_player_numbers = []

        shuffle(self.unused_player_numbers) # randomise the order of player numbers 

    def join(self, websocket: WebSocket) -> int:
        """
        Connect the websocket to the game

        Args:
            websocket: instance of WebSocket to be joined

        Returns:
            player number if successful, 0 otherwise
        """

        player = 0
        
        if not self.started:
            # take a player number available, assign it, and then take note of it
            player = self.connections[websocket] = self.unused_player_numbers.pop()
            self.used_player_numbers.append(player)

            # if there are no more player numbers available, start the game
            if len(self.unused_player_numbers) == 0:
                self.started = True
        
        return player

    async def send(self, websocket: WebSocket, message: Dict[str, object]) -> None:
        """
        Send a message in JSON to the websocket object

        Args:
            websocket: recipent for the message to be sent
            message: a valid JSON representation
        """

        await websocket.send_json(message)

    async def broadcast(self, message: Dict[str, object]) -> None:
        """
        Send a message in JSON to the all currently connected websockets

        Args:
            message: a valid JSON representation
        """

        for websocket in self.connections:
            await self.send(websocket, message)


    def remove(self, websocket: WebSocket, player: int) -> None:
        """
        Remove a currently connected websocket, and free the player number assigned to it

        Args:
            message: a valid JSON representation
        """

        self.connections.pop(websocket)
        self.unused_player_numbers.append(player)
        self.used_player_numbers.remove(player)


    async def exchange_names(self, player: int, nickname: str) -> None:
        """
        Send its nickname and player number to all other players

        Args:
            player: player number to be broadcasted
            nickname: nickname to be broadcasted alongside the player number
        """

        for websocket in self.connections:
            if self.connections[websocket] != player:
                await self.send(websocket, {
                    "event": "started",
                    "opponent": nickname
                })

class MultiPlayerBoardGame(Game):
    """
    Class used to create all multiplayer board games

    Attributes:
        dimensions: dictionary that maps column and row to their respecting size
        current_player: store the player number that can make a move at the current state of game
        is_over: whether the game is over or not
        vote_reset: set that stores all players that voted to reset the board
    """

    def __init__(self, room_id: str, players: int, row: int, col: int) -> None:
        """
        Constructor to instantiate an object of the class

        Args:
            room_id: id of the room being created
            row: number of rows in the board
            col: number of columns in the board
        """

        super().__init__(room_id, players) # call the superclass' constructor

        self.dimensions = {
            "row": row,
            "col": col
        }
        self.current_player = 1
        self.is_over = False
        self.vote_reset = set()
        
        self.create_board() # create a new board


    def create_board(self) -> None:
        """
            Create a fresh board initialised with 0's
        """

        self.board = [[0]*self.dimensions["row"] for _ in range(self.dimensions["col"])]

    def reset_board(self, player: int) -> None:
        """
            Reset the board if all players voted to reset it

            Args:
                player: the player calling the vote
        """

        flag = False

        self.vote_reset.add(player) # record the player calling a reset

        # reset the board if all player agree
        if len(self.vote_reset) == len(self.used_player_numbers): 
            self.create_board()
            self.current_player = choice(self.used_player_numbers) # chose a random player as the starting player
            self.vote_reset = set()
            self.is_over = False
            flag = True
        
        return flag