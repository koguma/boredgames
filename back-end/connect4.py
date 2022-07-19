from game import BoardGame, Player
from typing import Tuple

class Connect4(BoardGame):
    """
    Class for Connect4 logic

    Attributes:
        NORTH: relative coordinate to the adjacent square to the north
        SOUTH: relative coordinate to the adjacent square to the south
        WEST: relative coordinate to the adjacent square to the west
        EAST: relative coordinate to the adjacent square to the east
        NORTHWEST: relative coordinate to the adjacent square to the northwest
        SOUTHWEST: relative coordinate to the adjacent square to the southwest
        NORTHEAST: relative coordinate to the adjacent square to the northeast
        SOUTHEAST: relative coordinate to the adjacent square to the southeast
    """

    NORTH = (0,1)
    SOUTH = (0,-1)
    WEST = (-1,0)
    EAST = (1,0)
    NORTHWEST = (-1,1)
    NORTHEAST = (1,1)
    SOUTHEAST = (1,-1)
    SOUTHWEST = (-1,-1)

    def __init__(self, room_id : str) -> None:
        """
        Constructor
        
        Args:
            room_id: ID of the game being created
        """
        
        super().__init__(room_id, 2, 6, 7) # call the superclass' constructor

    def make_move(self, player: int, column: int) -> Tuple[int, Tuple[int,int]]:
        """
        Allow a player to make a move on the connect 4 board

        Args:
            player: player number making the move
            column: column the move should be played

        Returns:
            tuple containing the winner, and the coordinate of the move that was made
        """

        if not self.started:
            raise RuntimeError("The game has not started yet")

        if player != self.current_player:
            raise RuntimeError("It is not your turn yet")
        
        # loop through all squares in a column, find the first instance where it is 0 i.e. empty
        for i in reversed(range(self.dimensions["row"])):
            if self.board[column][i] == 0:
                self.board[column][i] = self.current_player
                coordinates = (column, i)
                break
        else:
            # check if no zero were found
            raise RuntimeError("The selected column is full")

        winner = 0
        
        # set the winner and is_over if the move played was a winning move
        if self.count_all_consecutive(player, coordinates[0], coordinates[1]) >= 3:
            winner = self.current_player
            self.is_over = True
        
        # otherwise, set winner as 3 i.e. draw and set is_over
        elif self.board_is_full():
            winner = 3
            self.is_over = True
        
        self.next_turn() # change to next turn

        return (winner, coordinates)

    def next_turn(self) -> None:
        """
        Change the current player
        """

        self.current_player = 1 if self.current_player == 2 else 2

    def board_is_full(self) -> bool:
        """
        Check if the board is full i.e. all the last square is filled in each and every column

        Returns:
            True if the board is full, False otherwise
        """

        return all(self.board[i][0] for i in range(self.dimensions["col"]))

    def count_all_consecutive(self, player: int, x: int, y: int) -> int:
        """
        Count the maximum number of connected pieces at the position

        Args:
            x: the x position of the square on the board
            y: the y position of the square on the board
        Returns:
            the count of the maximum consecutive connected pieces
        """
        
        return max([
            self.count_consecutive(player,x,y, Connect4.SOUTH) + self.count_consecutive(player,x,y, Connect4.NORTH), 
            self.count_consecutive(player,x,y, Connect4.WEST) + self.count_consecutive(player,x,y, Connect4.EAST), 
            self.count_consecutive(player,x,y, Connect4.SOUTHWEST) + self.count_consecutive(player,x,y, Connect4.NORTHEAST), 
            self.count_consecutive(player,x,y, Connect4.SOUTHEAST) + self.count_consecutive(player,x,y, Connect4.NORTHWEST)
            ])


    def count_consecutive(self, player: int, x: int, y: int, direction: Tuple[int,int]) -> int:
        """
        Count all consecutive player numbers on a square that matches the current player

        Args:
            x: the x position of the square on the board
            y: the y position of the square on the board
            direction: the square to which direction the function should check

        Returns:
            count of all consecutive player numbers stemming from the first call
        """
        
        # find the new x and y to the specified direction
        new_x = x + direction[0]
        new_y = y + direction[1]

        if new_x < 0 or new_y < 0: return 0

        # if it is a valid coordinate and the square is the same as current player number, then check further
        try:
            if self.board[new_x][new_y] == player:
                return 1 + self.count_consecutive(player, new_x,new_y,direction)

        except IndexError:
            pass
        
        return 0