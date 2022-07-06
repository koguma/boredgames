from game import MultiPlayerBoardGame
from typing import Tuple

class Piece:
    """
    Class used create a new checkers piece

    Attributes:
        owner: player number that controls this piece
        is_king: whether the piece has ascended to a king piece
    """

    def __init__(self, player: int) -> None:
        """
        Constructor

        Args:
            player: player number that should control this piece
        """

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
        switch = 1 
        for col in self.board:
            if switch:
                col[6] = Piece(2)
                col[0] = Piece(1)
                col[2] = Piece(1)
            else:
                col[1] = Piece(1)
                col[5] = Piece(2)
                col[7] = Piece(2)
            switch ^= 1 # bitwise XOR

    def next_turn(self) -> None:
        """
        Change the current player
        """

        self.current_player = 1 if self.current_player == 2 else 2

    def make_move(self, player: int, current_position: Tuple[int,int], future_position: Tuple[int,int]):
        """
        Allow a player to make a move on the checkers board

        Args:
            player: player number making the move
            current_position: column the move should be played

        Returns:
            TODO: figure out the implementation
        """

        if not self.started:
            raise RuntimeError("The game has not started yet")

        if player != self.current_player:
            raise RuntimeError("It is not your turn yet")
        
        x1, y1 = current_position
        x2, y2 = future_position
        
        try:
            piece = self.board[x1][y1]

            assert piece.owner == self.current_player
        
        except IndexError:
            raise RuntimeError("This is not a valid move")

        except AssertionError:
            raise RuntimeError("This is not your piece")
        
        except AttributeError:
            raise RuntimeError("There is no piece there")