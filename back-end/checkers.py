from asyncio import futures
from game import MultiPlayerBoardGame
from typing import Tuple

class Piece:
    def __init__(self, player: int) -> None:
        self.owner = player
        self.is_king = False

class Checkers(MultiPlayerBoardGame):

    def __init__(self, room_id : str) -> None:
        """
        Constructor to instantiate an object of the class

        Args:
            room_id: id of the room being created
        """

        super().__init__(room_id, 2, 8, 8) # call the superclass' constructor

        # initialise the board
        a = 1 
        for col in self.board:
            if a:
                col[6] = Piece(2)
                col[0] = Piece(1)
                col[2] = Piece(1)
            else:
                col[1] = Piece(1)
                col[5] = Piece(2)
                col[7] = Piece(2)
            a ^= 1 # bitwise XOR

    def next_turn(self) -> None:
        self.current_player = 1 if self.current_player == 2 else 2

    def make_move(self, player: int, current_position: Tuple(int,int), future_position: Tuple(int,int)):
        if not self.started:
            raise RuntimeError("The game has not started yet")

        if player != self.current_player:
            raise RuntimeError("It is not your turn yet")
        
        if not self.is_valid_move(current_position, future_position):
            raise RuntimeError("It is not a valid move")

        
    def is_valid_move(self, current_position : Tuple(int,int), future_position: Tuple(int,int)) -> bool:
        x1, y1 = current_position
        x2, y2 = future_position

        if (x1 < 0 or x1 > self.dimensions["col"]) or (x2 < 0 or x2 > self.dimensions["col"]): return False
        if (y1 < 0 or y1 > self.dimensions["row"]) or (y2 < 0 or y2 > self.dimensions["row"]): return False

        selected_piece = self.board[x1,y1]
        if type(selected_piece).__name__ != "Piece": return False
        
        return False