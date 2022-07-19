from typing import Dict, Optional
from fastapi import WebSocket
from random import shuffle, choice

class Player:

    def __init__(self, player: int, nickname: str, connection: Optional[WebSocket]):
        self.id = player
        self.nickname = nickname
        self.connection = connection
    
class Game:
    """
    The base class used to create all online games

    Attributes:
        connections: dictionary that maps connected websockets to their corresponding player number and nickname
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

        self.connections = []
        self.room_id = room_id 
        self.started = False
        self.dummy_plug = 0
        self.unused_player_numbers = [i+1 for i in range(num_of_players)]
        self.used_player_numbers = []

        shuffle(self.unused_player_numbers) # randomise the order of player numbers 

    async def join(self, websocket: Optional[WebSocket], nickname: str) -> Optional[Player]:
        """
        Connect the websocket to the game

        Args:
            websocket: instance of WebSocket to be joined
            nickname: nickname of the player

        Returns:
            player number if successful, 0 otherwise
        """

        player = None
        
        if not self.started:
            # take a player number available, assign it, and then take note of it
            player = Player(self.unused_player_numbers.pop(), nickname, websocket)
            self.connections.append(player)

            # notify the client of their player number
            await self.send(player, {
                "event": "connected",
                "you": player.id
            })

            self.used_player_numbers.append(player.id)

            # if there are no more player numbers available, start the game
            if len(self.unused_player_numbers) == 0:
                self.started = True

                if not player.connection:
                    self.dummy_plug = player.id

                # notify all players the opponent details e.g. player number, nickname
                if self.started:
                    message = {"event": "started"}
                    for p in self.connections:
                        message[p.id] = p.nickname
                    
                    await self.broadcast(message)
                    
        return player

    async def send(self, player: Player, message: Dict[str, object]) -> None:
        """
        Send a message in JSON to the websocket object

        Args:
            websocket: recipent for the message to be sent
            message: a valid JSON representation
        """

        if player.connection:
            await player.connection.send_json(message)

    async def broadcast(self, message: Dict[str, object]) -> None:
        """
        Send a message in JSON to the all currently connected websockets

        Args:
            message: a valid JSON representation
        """

        for player in self.connections:
            await self.send(player, message)


    def remove(self, player: Player) -> None:
        """
        Remove a currently connected websocket, and free the player number assigned to it

        Args:
            message: a valid JSON representation
        """

        self.connections.remove(player)
        self.unused_player_numbers.append(player.id)
        self.used_player_numbers.remove(player.id)

class BoardGame(Game):
    """
    Class used to create all board games

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

        if self.dummy_plug:
            self.vote_reset.add(self.dummy_plug)

        # reset the board if all player agree
        if len(self.vote_reset) == len(self.used_player_numbers): 
            self.create_board()
            self.current_player = choice(self.used_player_numbers) # chose a random player as the starting player
            self.vote_reset = set()
            self.is_over = False
            flag = True
        
        return flag