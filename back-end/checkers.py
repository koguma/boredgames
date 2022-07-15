import enum
from game import BoardGame
from typing import Dict, List, Optional, Tuple, Union

class Piece:
    """
    Class used create a new checkers piece

    Attributes:
        owner: player number that controls this piece
        is_king: whether the piece has ascended to a king piece
    """

    moves = {
        (1,1): (-2,-2),
        (-1,-1): (2,2),
        (1,-1): (-2,2),
        (-1,1): (2,-2)
    }

    moves_eat = [(-2,-2), (2,2), (-2,2), (2,-2)]

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

        self.init_board()

        self.force_eats = {
            1: [],
            2: []
        }

    def get_next_plauer(self) -> int:
        """
        Change the current player
        """

        return 1 if self.current_player == 2 else 2

    def get_all_eats(self, player: int) -> List[Dict[str,int]]:
        return self.force_eats[player]

    def reset_board(self, player):
        if super().reset_board(player):
            self.init_board()

    def init_board(self):

        self.count = {
            1: 12,
            2: 12
        }

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

    def is_won(self):
        return all(i == 0 for i in self.count) or all(i == 1 for i in self.count)

    def make_move(self, player: int, current_position: Tuple[int,int], future_position: Tuple[int,int]) -> Dict:
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
    
        is_valid, eaten = self.is_valid_move(player, current_position, future_position, testing=False)
        
        if is_valid:
            x1, y1 = current_position
            x2, y2 = future_position
            
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = 0
            
            if eaten:
                self.board[eaten[0]][eaten[1]] = 0
        
            self.update_force_eats(player, future_position)
            print(self.force_eats)

        else:
            raise RuntimeError("This is not a valid move")
        
        if self.is_won():
            self.is_over = True

        if ((eaten and len(self.force_eats[player]) == 0) or not eaten) and not self.is_over:
            self.current_player = self.get_next_plauer()

        new_board = [[0]*8 for _ in range(8)]
        for i,col in enumerate(self.board):
            for j,square in enumerate(col):
                try:
                    new_board[i][j] = square.owner
                except:
                    continue
            print(new_board[i])

        return {
            "previous_position": current_position,
            "current_position": future_position,
            "player": player,
            "next": self.current_player,
            "eaten": eaten,
            "king": self.board[x2][y2].is_king
        }

    def is_valid_move(self, player: int, current_position: Tuple[int,int], future_position: Tuple[int,int], middle_coord : Optional[Tuple[int,int]] = None, testing: bool = True) -> Tuple[bool, Optional[Tuple[int,int]]]:
        x1, y1 = current_position
        x2, y2 = future_position
        is_valid = False
        eaten = None

        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
            return (is_valid, eaten)

        if not testing and len(self.force_eats[player]) > 0 and all(current_position != move["current_position"] and future_position != move["future_position"] for move in self.force_eats[player]):
            print(current_position)
            print(future_position)
            return (is_valid, eaten)

        try:
            selected_piece = self.board[x1][y1]

            next_location = self.board[x2][y2]

            if selected_piece.owner == player and next_location == 0:
                displacement = (x1-x2,y1-y2)

                if displacement in Piece.moves_eat:
                    temp_x = x2+int(displacement[0]/2)
                    temp_y = y2+int(displacement[1]/2)
                    middle_piece = self.board[temp_x][temp_y]
            
                    if (middle_coord and middle_coord == (temp_x,temp_y)) or middle_piece.owner != player:
                        if (selected_piece.is_king
                            or selected_piece.owner == 1 and displacement[1] < 0
                            or selected_piece.owner == 2 and displacement[1] > 0):
                            is_valid = True
                            eaten = (temp_x,temp_y)

                elif displacement in Piece.moves:
                    if (selected_piece.is_king
                        or selected_piece.owner == 1 and displacement[1] < 0
                        or selected_piece.owner == 2 and displacement[1] > 0):
                        is_valid = True

                if is_valid and future_position[1] == 7 or future_position[1] == 0:
                    selected_piece.is_king = True

        except (IndexError, AttributeError):
            pass

        return (is_valid, eaten)

    def update_force_eats(self, player: int, current_position: Tuple[int,int]) -> None:
        x,y = current_position
        self.force_eats[player] = []
        next_player = self.get_next_plauer()   

        for x_displacement, y_displacement in Piece.moves_eat:
            future_position = (x+x_displacement, y+y_displacement)
            middle_position = (x+int(x_displacement/2), y+int(y_displacement/2))
            try:
                is_valid, _ = self.is_valid_move(player, current_position, future_position)
                if is_valid:
                    
                    self.force_eats[player].append({
                        "current_position": current_position,
                        "future_position": future_position
                    })

                    # for key in Piece.moves:
                    #     starting_position = (future_position[0]+key[0], future_position[1]+key[1])
                    #     corresponding_destination = (starting_position[0]+Piece.moves[key][0],starting_position[1]+Piece.moves[key][1])
                    #     try:

                    #         if self.is_valid_move(next_player, starting_position, corresponding_destination, middle_coord=middle_position):
                                
                    #             self.force_eats[next_player].append({
                    #                 "current_position": starting_position,
                    #                 "future_position": corresponding_destination
                    #             })

                    #     except (IndexError, AttributeError):
                    #         continue

            except (IndexError, AttributeError):
                continue

        if len(self.force_eats[player]) == 0:
            for key in Piece.moves:
                starting_position = (x+key[0], y+key[1])
                corresponding_destination = (starting_position[0]+Piece.moves[key][0],starting_position[1]+Piece.moves[key][1])

                try:
                    is_valid, _ = self.is_valid_move(next_player, starting_position, corresponding_destination)
                    if is_valid:
                        
                        self.force_eats[next_player].append({
                            "current_position": starting_position,
                            "future_position": corresponding_destination
                        })
                        print("why did this not work")

                except (IndexError, AttributeError):
                    continue