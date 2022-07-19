from collections import defaultdict
from game import BoardGame
from typing import Dict, List, Optional, Tuple, Union

class Piece:
    """
    Class used create a new checkers piece

    Attributes:
        owner: player number that controls this piece
        is_king: whether the piece has ascended to a king piece
        moves: possible default moves a piece can make
        moves_eat: possible eating moves a piece can make
    """

    moves = [
        (1,1),
        (-1,-1),
        (1,-1),
        (-1,1)
    ]

    moves_eat = [
        (2,-2),
        (-2,2),
        (2,2),
        (-2,-2)
    ]

    def __init__(self, player: int) -> None:
        """
        Constructor

        Args:
            player: player number that should control this piece
        """

        self.owner = player
        self.is_king = False

class Checkers(BoardGame):
    """
    Class used create a new checkers game

    Attributes:
        all_moves: dictionary containing all the moves that can currently be played on the board
    """

    def __init__(self, room_id : str) -> None:
        """
        Constructor to instantiate an object of the class

        Args:
            room_id: id of the room being created
        """

        super().__init__(room_id, 2, 8, 8) # call the superclass' constructor

        self.init_board()

    def init_board(self) -> None:
        """
            Initialise the board to its default state
        """

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

        self.calculate_all_moves()

    def get_next_plauer(self) -> int:
        """
        Get the next player in line

        Returns:
            the next player id
        """

        return 1 if self.current_player == 2 else 2

    def reset_board(self, player: int) -> bool:
        """
            Reset the board if all players voted to reset it

            Args:
                player: the player calling the vote
        """

        success = False
        
        # call the superclass' function and initialise the board
        if super().reset_board(player):
            self.init_board()
            success = True
        
        return success

    def get_possible_moves(self, player: int, current_position: Tuple[int,int]) -> List[Dict[str,Tuple[int,int]]]:
        """
            Get all the moves that can currently be played out on the board from the current position

            Returns:
                all the moves that can be played by the player's chosen piece
        """
        
        try:
            # prioritise eating moves (force eats)
            if len(self.all_moves["moves_eat"][player]) > 0:
                return self.all_moves["moves_eat"][player][current_position]
            
            # otherwise, return the normal moves
            return self.all_moves["moves"][player][current_position]
            
        except KeyError:
            return []

    def calculate_all_moves(self, previous_was_eat: Optional[Tuple[int,int]] = None) -> None:
        """
            Calculate all the moves that can currently be played out on the board

            Args:
                previous_was_eat: if the previous move was eat, then make sure the only availahle eat is the continuation of the previous eat
        """

        # Reset the dictionary of moves that can be made on the current 
        self.all_moves = {
            "moves_eat": {player: {} for player in [1,2]},
            "moves": {player: {} for player in [1,2]},
        }

        # for every piece (square) on the board, get the player number owning the piece
        for x, col in enumerate(self.board):
            for y, piece in enumerate(col):
                try:
                    player = piece.owner
                except AttributeError:
                    continue
                
                current_position = (x,y)

                self.find_valid_moves(player, current_position, Piece.moves_eat, "moves_eat")
                self.find_valid_moves(player, current_position, Piece.moves, "moves")

        if previous_was_eat and previous_was_eat in self.all_moves["moves_eat"][self.current_player]:
            
            new_dict = {key: self.all_moves["moves_eat"][self.current_player][key] for key in self.all_moves["moves_eat"][self.current_player] if key == previous_was_eat}
            
            self.all_moves["moves_eat"][self.current_player] = new_dict

    def find_valid_moves(self, player: int, current_position: Tuple[int,int], lst: List[Tuple[int,int]], key: str) -> None:
        """
        Find all the valid moves that can be played out from the current_position

        Args:
            player: player number making the move
            current_position: position on the board of the chosen piece
            lst: list of valid coordinates to be checked
            key: name of the key in all_moves dictionary
        
        Returns:
            True if there are valid moves False otherwise
        """

        x,y = current_position

        # call the is_valid_move function for every possible moves
        for x_displacement, y_displacement in lst:
            future_position = (x+x_displacement, y+y_displacement)

            is_valid, _ = self.is_valid_move(current_position, future_position)
            
            if is_valid:

                # create an empty list if it doesn't exist
                if current_position not in self.all_moves[key][player]:
                    self.all_moves[key][player][current_position] = []

                # append a new dictionary listing the possible moves
                self.all_moves[key][player][current_position].append({
                    "possible_move": future_position,
                })
        
        return True if current_position in self.all_moves[key][player] else False

    def make_move(self, player: int, current_position: Tuple[int,int], future_position: Tuple[int,int]) -> Tuple[Dict[str,object],int]:
        """
        Allow a player to make a move on the checkers board

        Args:
            player: player number making the move
            current_position: position on the board of the chosen piece
            future_position: resulting position of the chosen piece on the board after the move

        Returns:
            tuple containing the move details and the winner details
        """

        if not self.started:
            raise RuntimeError("The game has not started yet")

        if player != self.current_player:
            raise RuntimeError("It is not your turn yet")
    
        # check if move is valid
        is_valid, eaten = self.is_valid_move(current_position, future_position, testing=False)
        
        if is_valid:
            x1, y1 = current_position
            x2, y2 = future_position
            
            # move the piece
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = 0
            
            # if eaten, change the middle piece to 0
            if eaten:
                self.board[eaten[0]][eaten[1]] = 0

        else:
            raise RuntimeError("This is not a valid move")
        
        # recalculate all the possible moves after the move was made
        self.calculate_all_moves(future_position)
        
        # get all the players that can no longer make a move
        players_that_cannnot_make_moves = [i for i in self.used_player_numbers if len(self.all_moves["moves_eat"][i]) == 0 and len(self.all_moves["moves"][i]) == 0]
        
        winner = 0
        
        if len(players_that_cannnot_make_moves) > 0:
            # if no possible moves by a player, then the game is over
            self.is_over = True

            # if both players cannot make a move, it is a draw
            if len(players_that_cannnot_make_moves) == 2:
                winner = 3
            elif players_that_cannnot_make_moves[0] == 1:
                winner = 2
            else:
                winner = 1

        # if there is no force eats, then change turn
        if (eaten and len(self.all_moves["moves_eat"][player]) == 0 or not eaten) and not self.is_over:
            self.current_player = self.get_next_plauer()

        return ({
            "previous_position": current_position,
            "current_position": future_position,
            "player": player,
            "next": self.current_player,
            "eaten": eaten,
            "king": self.board[x2][y2].is_king
        },winner)

    def is_valid_move(self, current_position: Tuple[int,int], future_position: Tuple[int,int], testing: bool = True, assume_middle_piece: bool = False) -> Tuple[bool, Optional[Tuple[int,int]]]:
        
        x1, y1 = current_position
        x2, y2 = future_position
        is_valid = False
        eaten = None
        
        # don't accept any negative indexes for the board as it will cause error
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0: return (is_valid, eaten)

        try:
            selected_piece = self.board[x1][y1]
            player = selected_piece.owner

            # if the move is being played and not tested, then prioritise force eats
            if not testing:
                if len(self.all_moves["moves_eat"][player]) > 0:
                    if current_position not in self.all_moves["moves_eat"][player] or not any((future_position == move["possible_move"]) for move in self.all_moves["moves_eat"][player][current_position]):
                        return (is_valid, eaten)

            next_location = self.board[x2][y2]

            # destination should be an emtpy square
            if next_location == 0:
                displacement = (x1-x2,y1-y2)

                # if the move is an eating move, make sure the middle piece is of opposite player, and that the move itself is valid
                if displacement in Piece.moves_eat:
                    temp_x = x2+int(displacement[0]/2)
                    temp_y = y2+int(displacement[1]/2)
                    middle_piece = self.board[temp_x][temp_y]
            
                    if assume_middle_piece or middle_piece.owner != player:
                        if (selected_piece.is_king
                            or selected_piece.owner == 1 and displacement[1] < 0
                            or selected_piece.owner == 2 and displacement[1] > 0):
                            is_valid = True
                            eaten = (temp_x,temp_y)

                # if the move is a normal move, make sure that the move itself is valid
                elif displacement in Piece.moves:
                    if (selected_piece.is_king
                        or selected_piece.owner == 1 and displacement[1] < 0
                        or selected_piece.owner == 2 and displacement[1] > 0):
                        is_valid = True

                # if the move is being played and not tested, then upgrade the piece to king if it satisfies the conditions
                if not testing and is_valid and (future_position[1] == 7 or future_position[1] == 0) and not selected_piece.is_king:
                    selected_piece.is_king = True

        except (IndexError, AttributeError):
            pass

        return (is_valid, eaten)