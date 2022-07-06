from game import MultiPlayerBoardGame
from typing import Tuple

class Connect4(MultiPlayerBoardGame):
    """
    Class for Connect4 logic
    """

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
                coords = (column, i)
                break
        else:
            # check if no zero were found
            raise RuntimeError("The selected column is full")

        winner = 0
        
        # set the winner and is_over if the move played was a winning move
        if self.is_vertical_win(coords) or self.is_horizontal_win(coords) or self.is_diagonal_win(coords):
            winner = self.current_player
            self.is_over = True
        
        # otherwise, set winner as 3 i.e. draw and set is_over
        elif self.board_is_full():
            winner = 3
            self.is_over = True
        
        self.next_turn() # change to next turn

        return (winner, coords)

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

    def is_diagonal_win(self, coords: Tuple[int, int]) -> bool:
        """
        Check if the move at the coordinate has a diagonal win fgor the current player

        Args:
            coords: coordinate of the move that should be checked

        Returns:
            True if the move was a diagonal win, False otherwise
        """

        x,y = coords # assign x and y from the tuple

        # if there is 4 consecutive current player number with the check going like "/", then there is a win
        count = 1 + self.diagonal_forward_count(x+1, y+1, True) + self.diagonal_forward_count(x-1, y-1, False)
        if count >= 4: return True

        # if there is 4 consecutive current player number with the check going like "/", then there is a win
        count = 1 + self.diagonal_backward_count(x-1, y+1, True) + self.diagonal_backward_count(x+1, y-1, False)
        return count >= 4

    def is_vertical_win(self, coords: Tuple[int, int]) -> bool:
        """
        Check if the move at the coordinate has a vertical win fgor the current player

        Args:
            coords: coordinate of the move that should be checked

        Returns:
            True if the move was a vertical win, False otherwise
        """

        x,y = coords # assign x and y from the tuple

        # if there is 4 consecutive current player number with the check, then there is a win
        count = 1 + self.vertical_count(x, y+1, True) + self.vertical_count(x, y-1, False)
        return count >= 4

    def is_horizontal_win(self, coords: Tuple[int, int]) -> bool:
        """
        Check if the move at the coordinate has a horizontal win fgor the current player

        Args:
            coords: coordinate of the move that should be checked

        Returns:
            True if the move was a horizontal win, False otherwise
        """

        x,y = coords # assign x and y from the tuple

        # if there is 4 consecutive current player number with the check, then there is a win
        count = 1 + self.horizontal_count(x-1, y, True) + self.horizontal_count(x+1, y, False)
        return count >= 4

    def diagonal_backward_count(self, x: int, y: int, up: bool) -> int:
        """
        Count all consecutive player numbers on a square diagonally like "\"

        Args:
            x: the x position of the square on the board
            y: the y position of the square on the board
            up: whether it should check up or down

        Returns:
            count of all consecutive player numbers stemming from the first input
        """
        
        # return 0 if it is no longer the player number or out of index, otherwise, keep going up or down
        try:
            if self.board[x][y] == self.current_player:
                if up:
                    return 1 + self.diagonal_backward_count(x-1,y+1,up)
                else:
                    return 1 + self.diagonal_backward_count(x+1,y-1,up)
        except IndexError:
            pass
        return 0

    def diagonal_forward_count(self, x: int, y: int, up: bool) -> int:
        """
        Count all consecutive player numbers on a square diagonally like "/"

        Args:
            x: the x position of the square on the board
            y: the y position of the square on the board
            up: whether it should check up or down

        Returns:
            count of all consecutive player numbers stemming from the first input
        """
       
        # return 0 if it is no longer the player number or out of index, otherwise, keep going up or down
        try:
            if self.board[x][y] == self.current_player:
                if up:
                    return 1 + self.diagonal_forward_count(x+1,y+1,up)
                else:
                    return 1 + self.diagonal_forward_count(x-1,y-1,up)
        except IndexError:
            pass
        return 0

    def vertical_count(self, x: int, y: int, up: bool) -> int:
        """
        Count all consecutive player numbers on a square vertically

        Args:
            x: the x position of the square on the board
            y: the y position of the square on the board
            up: whether it should check up or down

        Returns:
            count of all consecutive player numbers stemming from the first input
        """

        # return 0 if it is no longer the player number or out of index, otherwise, keep going up or down
        try:
            if self.board[x][y] == self.current_player:
                if up:
                    return 1 + self.vertical_count(x, y+1, up)
                else:
                    return 1 + self.vertical_count(x, y-1, up)
        except IndexError:
            pass
        return 0

    def horizontal_count(self, x: int, y: int, left: bool) -> int:
        """
        Count all consecutive player numbers on a square horizontally

        Args:
            x: the x position of the square on the board
            y: the y position of the square on the board
            left: whether it should check left or right

        Returns:
            count of all consecutive player numbers stemming from the first input
        """

        # return 0 if it is no longer the player number or out of index, otherwise, keep going left or right
        try:
            if self.board[x][y] == self.current_player:
                if left:
                    return 1 + self.horizontal_count(x-1, y, left)
                else:
                    return 1 + self.horizontal_count(x+1, y, left)
        except IndexError:
            pass
        return 0