from game import BoardGame
from typing import Dict, Tuple

class Piece:
    """
    Class used create a new checkers piece

    Attributes:
        owner: player number that controls this piece
        is_king: whether the piece has ascended to a king piece
    """

    moves = [(1,1),(-1,1),(1,-1),(-1,-1)]
    moves_eat = [(2*i,2*j) for i,j in moves]

    def __init__(self, player: int) -> None:
        """
        Constructor

        Args:
            player: player number that should control this piece
        """

        self.owner = player
        self.is_king = False

class Checkers(BoardGame):

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

        self.force_eats = {
            1: [],
            2: []
        }

    def next_turn(self) -> None:
        """
        Change the current player
        """

        self.current_player = 1 if self.current_player == 2 else 2

    def make_move(self, player: int, current_position: Tuple[int,int], future_position: Tuple[int,int]) -> Tuple[int,Dict]:
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
        
        move = {
            "previous_position": current_position,
            "next_position": future_position,
        }
    
        try:
            x1, y1 = current_position
            x2, y2 = future_position
            
            selected_piece = self.board[x1][y1]
            next_location = self.board[x2][y2]

            if selected_piece.owner != player:
                raise RuntimeError("This is not your piece")

            if next_location != 0:
                raise RuntimeError("There is already a piece there")
            
            displacement = (x1-x2,y1-y2)

            if not selected_piece.is_king and ((selected_piece.owner == 1 and displacement[1] < 0) or (selected_piece.owner == 2 and displacement[1] > 0)):
                raise RuntimeError("The piece cannot go backward")

            if displacement in Piece.moves_eat:
                x3 = x1 + displacement[0]
                y3 = y1 + displacement[1]

                if displacement[0] > 0:
                    x3 -= 1
                else:
                    x3 += 1
                
                if displacement[1] > 0:
                    y3 -= 1
                else:
                    y3 += 1
                
                middle_piece = self.board[x3,y3]
                
                if middle_piece.owner != self.current_player:
                    raise RuntimeError("You cannot eat your own piece")

                move["eaten"] = (x3,y3)

            elif displacement not in Piece.moves:
                raise RuntimeError("This is not a valid move")

            self.board[x2][y2] = selected_piece
            self.board[x1][y1] = 0

            self.update_force_eats(x2,y2)
            self.next_turn()
        
        except (IndexError, AttributeError):
            raise RuntimeError("This is not a valid move")

        return move

    def is_valid_move(self, x: int, y: int):
        pass
    
    def update_force_eats(self, x: int, y: int) -> None:
        
        for i, (x_displacement, y_displacement) in enumerate(Piece.moves):
            adjacent_x = x + x_displacement
            adjacent_y = y + y_displacement

            try:
                if self.board[adjacent_x][adjacent_y].owner != self.current_player:
                    next_x, next_y = Piece.moves_eat[i]
                    next_piece = self.board[next_x][next_y]
                    
                    if self.is_valid_move(next_x,next_y):
                        if next_piece == 0:
                            self.force_eats[self.current_player].append(tuple(next_x, next_y))
                        
                        elif next_piece.owner != self.current_player:
                            self.force_eats[self.next_piece.owner].append()
            
            except (IndexError, AttributeError):
                pass