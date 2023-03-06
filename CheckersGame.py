# Author: Larry Urrego
# GitHub username: LaUrrego
# Date:
# Description: Checkers simulator...


class IncorrectColorPieceError(Exception):
    """Used to validate player creation with piece color as string 'Black' or 'White'"""
    pass


class OutofTurn(Exception):
    pass


class InvalidSquare(Exception):
    pass


class InvalidPlayer(Exception):
    pass


class CheckerBoard:

    def __init__(self):
        # initiate board with "OK" for valid black squares and None for invalid white squares
        new_board = self.filler("OK", None)
        # board data member
        self._board = new_board
        # Sets up board with player pieces
        self.start_setup()

    def get_board(self):
        return self._board

    def filler(self, color1, color2):
        """Fills a board array with 8 rows and 8 columns using two specified fillers"""
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
        """Sets up the board with top three rows White, bottom 3 rows Black"""
        # set White
        for row in range(3):
            for column in range(8):
                if self._board[row][column] == "OK":
                    self._board[row][column] = "White"
        # set Black
        for row in range(3):
            for column in range (8):
                if self._board[row + 5][column] == "OK":
                    self._board[row + 5][column] = "Black"



class Checkers:
    """
    information about the  board and the players. Board initialized when this object is created.
    position is: (row, column)
    """
    def __init__(self):
        # initialized as "Black" for first move
        self._current_turn = "Black"
        self._players = {}
        board = CheckerBoard()
        self._current_board = board.get_board()

    def change_turn(self):
        """Function to change the color piece going next"""
        if self._current_turn == "Black":
            self._current_turn = "White"
        elif self._current_turn == "White":
            self._current_turn = "Black"
        return

    def valid_turn(self, player_name):
        if self._players[self._current_turn] == player_name:
            return True
        return False

    def get_square_details(self, position):
        """Details on whether the square is None, White, Black, or OK"""
        return self._current_board[position[0]][position[1]]

    def get_color(self, name):
        """Get method for the color of the player provided as input"""
        for key, value in self._players.items():
            if value == name:
                return key

    def valid_square_location(self, position):
        """Returns true square coordinates are valid, false if None, or raises InvalidSquare
        if not valid"""
        try:
            # Space is a white square
            if self._current_board[position[0]][position[1]] is None:
                return False
            # Space is a black square
            elif self._current_board[position[0]][position[1]]:
                return True
            # outside of the board
        except IndexError:
            raise InvalidSquare("This position does not exist")

    def create_player(self, player_name, piece_color):
        if piece_color.lower() == "black":
            self._players["Black"] = player_name
            return Player(player_name,"Black")
        elif piece_color.lower() == "white":
            self._players["White"] = player_name
            return Player(player_name, "White")
        else:
            raise IncorrectColorPieceError("Piece color can only be 'White' or 'Black'!")

    def play_game(self, player_name, starting_square_location, destination_square_location):
        if not self.valid_turn(player_name):
            raise OutofTurn("It's not currently your turn!")
        else:
            # raises InvalidSquare if outside the board
            check_start = self.valid_square_location(starting_square_location)
            check_dest = self.valid_square_location(destination_square_location)
            # raises InvalidSquare if a white "None" square
            if not check_start or not check_dest:
                raise InvalidSquare("Not a valid choice!")
            current_player = self.get_color(player_name)
            square_owner = self.get_square_details(starting_square_location)
            # raises InvalidSquare if current player is not the owner of the starting location
            if current_player != square_owner:
                raise InvalidSquare("This is not your piece!")
            #### continue with If the player_name is not valid, raise an InvalidPlayer exception (you'll need to define this exception class).

    def get_checker_details(self):
        pass

    def print_board(self):
        """Prints the current game board in the form of an array"""
        return self._current_board

    def game_winner(self):
        pass


class Player:

    def __init__(self, player_name, checker_color):
        self._player_name = player_name
        self._checker_color = checker_color

    def get_checker_color(self):
        return self._checker_color

    def get_king_count(self):
        pass

    def get_triple_king_count(self):
        pass

    def get_captured_pieces_count(self):
        pass


#board = CheckerBoard()
game = Checkers()
print(game.valid_square_location((0,0)))
game.create_player("Larry", "black")
game.create_player("Karolcia", "white")
game.play_game("Larry", (7,0), (0,1))
for row in game.print_board():
    print(row)