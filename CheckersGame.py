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


class Token:
    """Represents a checkers piece token. Can take the form of a regular piece, King or Triple King. Includes
    methods to move it based on official rules"""
    def __init__(self, position, color):
        # can be "Regular", "King" or "TripleKing"
        self._type = "Regular"
        self._current_position = position
        self._color = color

    def move(self, start_position, end_position, game_board):
        if self._type == "Regular":
            pass

    def get_position(self):
        """Return where this token is current placed"""
        return self._current_position

    def get_possible_moves(self, game_board):
        """Returns possible moves for this token"""
        row, column = self._current_position
        possible_moves = []
        if self._type == "Regular":
            # black piece logic
            if self._color == "Black":
                if row == 0:
                    print("TOP EDGE, CHANGE TO KING")
                    return
                row_above = game_board[row - 1]
                # Search for potential adjacent enemy piece
                if row_above[column + 1] == "White" or row_above[column - 1] == "White":
                    # only two possible pieces adjacent to current token
                    adjacent_candidate = []
                    for index, square in enumerate(game_board[row - 1]):
                        # white piece adjacent
                        if square == "White" and (index == column + 1 or index == column - 1) and row > 1:
                            # add candidates
                            adjacent_candidate.append((row-1, index))
                    print("adjacent: ", adjacent_candidate)
                    two_above = game_board[row - 2]
                    for candidates in adjacent_candidate:
                        x_pos, y_pos = candidates
                        # on the right
                        if y_pos > column:
                            if two_above[y_pos + 1] == "OK":
                                possible_moves.append((row-2, y_pos + 1))
                        # on the left
                        elif y_pos < column:
                            if two_above[y_pos - 1] == "OK":
                                possible_moves.append((row-2, y_pos - 1))
                    return possible_moves
                # No white in row above piece
                else:
                    for index, square in enumerate(game_board[row - 1]):
                        if square == "OK" and (index == column + 1 or index == column - 1):
                            # add empty space not occupied by enemy or None
                            possible_moves.append((row - 1, index))
                return possible_moves

            # white piece logic
            elif self._color == "White":
                pass





class CheckerBoard:
    """Class simulating a checkerboard object. Has methods to create a board as well as fill it with white and black
    tokens to begin gameplay"""
    def __init__(self):
        # initiate board with "OK" for valid black squares and None for invalid white squares
        new_board = self.filler("OK", None)
        # board data member
        self._board = new_board

    def get_board(self):
        """Get method to return the current board"""
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


class Checkers:
    """
    information about the  board and the players. Board initialized when this object is created.
    position is: (row, column)
    """
    def __init__(self):
        # initialized as "Black" for first move
        self._current_turn = "Black"
        self._players = {}
        self._tokens = {
            "Black": [],
            "White": [],
        }
        self._current_board = None
        self.setup()

    def test_adder(self, color, pos):
        """tester method to add a piece in a particular place"""
        row, column = pos
        self._current_board[row][column] = color
        return

    def setup(self):
        """Sets up the board with pieces and fills token collection for each player"""
        board = CheckerBoard()
        pieces = board.start_setup()
        # fill white pieces
        for item in pieces[0]:
            self._tokens["White"].append(item)
        # fill black pieces
        for item in pieces[1]:
            self._tokens["Black"].append(item)
        self._current_board = board.get_board()


    def change_turn(self):
        """Function to change the color piece going next"""
        if self._current_turn == "Black":
            self._current_turn = "White"
        elif self._current_turn == "White":
            self._current_turn = "Black"
        return

    def valid_player(self, player_name):
        """Checks to see if input name is the currently allowed player to move"""
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
        """Creates a player given a name and piece color. Returns the player object"""
        if piece_color.lower() == "black":
            self._players["Black"] = player_name
            return Player(player_name,"Black")
        elif piece_color.lower() == "white":
            self._players["White"] = player_name
            return Player(player_name, "White")
        else:
            raise IncorrectColorPieceError("Piece color can only be 'White' or 'Black'!")

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """Nie Wiem"""
        if not self.valid_player(player_name):
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
            if player_name not in self._players.values():
                raise InvalidPlayer("This is not a valid player!")
            # should match one of the current pieces in play
            for tokens in self._tokens[self._current_turn]:
                if tokens.get_position() == starting_square_location:
                    # test to see possible moves
                    print(tokens.get_possible_moves(self._current_board))
                    return


            #### continue with If the player_name is not valid, raise an InvalidPlayer exception (you'll need to define this exception class).

    def get_checker_details(self):
        pass

    def print_board(self):
        """Prints the current game board in the form of an array"""
        return self._current_board

    def game_winner(self):
        pass


class Player:
    """Simulates a player in checkers, initialized with a player_name and checker_color. Includes methods to return
    the color, capture count, number of king pieces, and number of triple king pieces"""
    def __init__(self, player_name, checker_color):
        self._player_name = player_name
        self._checker_color = checker_color

    def get_checker_color(self):
        """Returns the players checker color"""
        return self._checker_color

    def get_king_count(self):
        """Returns the number of kings this player has"""
        pass

    def get_triple_king_count(self):
        """Returns the number of triple kings this player has"""
        pass

    def get_captured_pieces_count(self):
        """Returns the amount of captures pieces by the current player"""
        pass


#board = CheckerBoard()
game = Checkers()
print(game.valid_square_location((0,0)))
game.create_player("Larry", "black")
game.create_player("Karolcia", "white")
#game.test_adder("White", (4,3))
#game.test_adder("White", (4,1))
game.play_game("Larry", (5,0), (4,1))
for row in game.print_board():
    print(row)

#for color, token in game._tokens.items():
#    print(color)
#    for piece in token:
#        print(piece.get_position())