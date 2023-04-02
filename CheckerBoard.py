from Token import Token

class CheckerBoard:
    """Class simulating a checkerboard object. Has methods to create a board as well as fill it with white and black
    tokens to begin gameplay"""
    def __init__(self):
        # initiate board with "OK" for valid black squares and None for invalid white squares
        new_board = self.filler("OK", None)
        # board data member
        self._board = new_board

    def get_board(self):
        """
        Get method to return the current board"

        :return: Array of arrays
        """
        return self._board

    def filler(self, color1, color2):
        """
        Fills a board array with 8 rows and 8 columns using two specified fillers

        :param color1: String (typically corresponds to "OK")
        :param color2: String (Typically corresponds to None)
        :return: array of arrays representing rows with white and black squares of a checkerboard
        """
        board = []
        for row in range(8):
            if row % 2 == 0:
                whole_row = []
                for column in range(8):
                    if column % 2 == 0:
                        whole_row.append(color2)
                    else:
                        whole_row.append(color1)
                board.append(whole_row)
            else:
                whole_row = []
                for column in range(8):
                    if column % 2 == 0:
                        whole_row.append(color1)
                    else:
                        whole_row.append(color2)
                board.append(whole_row)
        return board

    def start_setup(self):
        """
        Sets up the board with top three rows White, bottom 3 rows Black

        :return: Array of arrays
        """
        # set White
        white_tokens = []
        for row in range(3):
            for column in range(8):
                if self._board[row][column] == "OK":
                    self._board[row][column] = "White"
                    white_tokens.append(Token((row, column), "White"))
        # set Black
        black_tokens = []
        for row in range(3):
            for column in range (8):
                if self._board[row + 5][column] == "OK":
                    self._board[row + 5][column] = "Black"
                    black_tokens.append(Token((row + 5, column), "Black"))
        return [white_tokens, black_tokens]