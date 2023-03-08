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

    def change_position(self, position):
        """changes token's current position"""
        self._current_position = position

    def change_type(self, type):
        """changes the token's current type"""
        self._type = type

    def get_position(self):
        """Return where this token is current placed"""
        return self._current_position

    def get_type(self):
        return self._type

    def get_possible_moves(self, game_board):
        """Returns possible moves for this token"""
        row, column = self._current_position
        possible_moves = []
        if self._type == "Regular":
            # black piece logic
            if self._color == "Black":
                #if row == 0:
                #    print("TOP EDGE, CHANGE TO KING")
                #    return
                row_above = game_board[row - 1]
                # Search for potential adjacent enemy piece
                # test for edge of board
                if column == 7:
                    condition = row_above[column - 1] == "White"
                else:
                    condition = row_above[column + 1] == "White" or row_above[column - 1] == "White"
                if condition:
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
                #if row == 7:
                #   print("BOTTOM EDGE, CHANGE TO KING")
                #    return
                row_below = game_board[row + 1]
                # Search for potential adjacent enemy piece
                # test for edge of board
                if column == 7:
                    condition = row_below[column - 1] == "Black"
                else:
                    condition = row_below[column - 1] == "Black" or row_below[column + 1] == "Black"
                if condition:
                    # only two possible pieces adjacent to current token
                    adjacent_candidate = []
                    for index, square in enumerate(game_board[row + 1]):
                        # black piece adjacent
                        if square == "Black" and (index == column + 1 or index == column - 1) and row < 6:
                            # add candidates
                            adjacent_candidate.append((row + 1, index))
                    print("adjacent: ", adjacent_candidate)
                    two_below = game_board[row + 2]
                    for candidates in adjacent_candidate:
                        x_pos, y_pos = candidates
                        # on the right
                        if y_pos > column:
                            if two_below[y_pos + 1] == "OK":
                                possible_moves.append((row + 2, y_pos + 1))
                        # on the left
                        elif y_pos < column:
                            if two_below[y_pos - 1] == "OK":
                                possible_moves.append((row + 2, y_pos - 1))
                    return possible_moves
                # No black in row above piece
                else:
                    for index, square in enumerate(game_board[row + 1]):
                        if square == "OK" and (index == column + 1 or index == column - 1):
                            # add empty space not occupied by enemy or None
                            possible_moves.append((row + 1, index))
                return possible_moves
        elif self._type == "King":
            # black_king piece logic
            if self._color == "Black":
                # can move one forwards or backwards for non capture
                # when possible to capture, can go on any diagonal space as long as only 1 is captured
                # no need for enemies to be adjacent
                #row, column = self._current_position /// remember from top
                #possible_moves = [] /// remember from top
                #diagonal_above_left = []
                #for index in range(1, min(row, column) + 1):
                #    current = game_board[row - index][column - index]
                #    if current == "OK" or current == "White":
                #        diagonal_above_left.append((row - index, column - index))
                #print(diagonal_above_left)

                #diagonal_above_right = []
                #for index in range(1, min(row, 8 - column) ):
                #    current = game_board[row - index][column + index]
                #    if current == "OK" or current == "White":
                #        diagonal_above_right.append((row - index, column + index))
                #print(diagonal_above_right)

                #diagonal_bottom_right = []
                #for index in range(1, min(8 - row, 8 - column)):
                #    current = game_board[row + index][column + index]
                #    if current == "OK" or current == "White":
                #        diagonal_bottom_right.append((row + index, column + index))
                #print(diagonal_bottom_right)

                #diagonal_bottom_left = []
                #for index in range(1, min(8 - row, column)):
                #    current = game_board[row + index][column - index]
                #    if current == "OK" or current == "White":
                #        diagonal_bottom_left.append((row + index, column - index))
                #print(diagonal_bottom_left)

                #possible_moves = [diagonal_above_left,
                #                  diagonal_bottom_right,
                #                  diagonal_above_right,
                #                  diagonal_bottom_left]
                #return possible_moves
                return self.king_move_logic("White", row, column, game_board)

            # white_king piece logic
            elif self._color == "White":
                return self.king_move_logic("Black", row, column, game_board)

        elif self._type == "TripleKing":
            return "TripleKing" # remove

    def king_move_logic(self, color, row_pos, column_pos, board):
        """Takes a color of the enemy piece, row position, column position and current game board
        Returns a list of possible open spaces and identified enemy pieces for used in self.game_play()"""
        diagonal_above_left = []
        for index in range(1, min(row_pos, column_pos) + 1):
            current = board[row_pos - index][column_pos - index]
            if current == "OK" or current == color:
                diagonal_above_left.append((row_pos - index, column_pos - index))
        print(diagonal_above_left)

        diagonal_above_right = []
        for index in range(1, min(row_pos, 8 - column_pos)):
            current = board[row_pos - index][column_pos + index]
            if current == "OK" or current == color:
                diagonal_above_right.append((row_pos - index, column_pos + index))
        print(diagonal_above_right)

        diagonal_bottom_right = []
        for index in range(1, min(8 - row_pos, 8 - column_pos)):
            current = board[row_pos + index][column_pos + index]
            if current == "OK" or current == color:
                diagonal_bottom_right.append((row_pos + index, column_pos + index))
        print(diagonal_bottom_right)

        diagonal_bottom_left = []
        for index in range(1, min(8 - row_pos, column_pos)):
            current = board[row_pos + index][column_pos - index]
            if current == "OK" or current == color:
                diagonal_bottom_left.append((row_pos + index, column_pos - index))
        print(diagonal_bottom_left)

        moves = [diagonal_above_left, diagonal_bottom_right, diagonal_above_right, diagonal_bottom_left]
        return moves

    def possible_jumps(self, moves_list, board):
        """Takes a current position and possible moves list. If a jump is possible, returns True, else False"""
        if self._type == "Regular":
            pass
        elif self._type == "King":
            jumps = 0
            for diagonal in moves_list:
                translated_list = []
                if len(diagonal) == 0:
                    pass
                for move in diagonal:
                    row, column = move
                    translated_list.append(board[row][column])
                print("translated list: ", translated_list)
                for space in range(len(translated_list)):
                    if translated_list[space] == "OK":
                        continue
                    elif translated_list[space] != "OK":
                        if space < (len(translated_list) - 1) and translated_list[space + 1] == "OK":
                            jumps += 1
            return jumps




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

    def get_white_tokens(self):
        return self._tokens["White"]

    def get_black_tokens(self):
        return self._tokens["Black"]

    def test_color_change(self, color):
        """Changes the current turn for testing purposes"""
        self._current_turn = color

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
                    # test to make king once we have the selected piece
                    tokens.change_type("King")
                    # test to see possible moves
                    moves = tokens.get_possible_moves(self._current_board)
                    print("Pre-Move___________________________________________________________________")
                    print(tokens.get_possible_moves(self._current_board))
                    # test to translate moves visually
                    print("possible jumps: ",tokens.possible_jumps(moves, self._current_board))
                    print("Post-Move__________________________________________________________________")

            #### continue with moving and returning any pieces


    def get_checker_details(self, square_location):
        """takes a position on the board and returns the type of token currently on it or None if empty"""
        row, column = square_location
        selected = self._current_board[row][column]
        if selected is None or selected == "OK":
            return None
        for piece in self.get_white_tokens():
            if piece.get_position() == square_location:
                if piece.get_type() == "Regular":
                    return "White"
                elif piece.get_type() == "King":
                    return "White_king"
                elif piece.get_type() == "TripleKing":
                    return "White_Triple_King"
        for piece in self.get_black_tokens():
            if piece.get_position() == square_location:
                if piece.get_type() == "Regular":
                    return "Black"
                elif piece.get_type() == "King":
                    return "Black_king"
                elif piece.get_type() == "TripleKing":
                    return "Black_Triple_King"

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
game.create_player("Larry", "black")
game.create_player("Karolcia", "white")
#game.test_adder("White", (4,5))
#game.test_adder("White", (3,6))
#game.test_color_change("White")
game.play_game("Larry", (5,4), (4,1))

for row in game.print_board():
    new_row = []
    for piece in row:
        if piece == "White":
            new_row.append("W")
        elif piece == "Black":
            new_row.append("B")
        elif piece == "OK":
            new_row.append("_")
        elif piece is None:
            new_row.append("X")
    print(new_row)

#for color, token in game._tokens.items():
#    print(color)
#    for piece in token:
#        print(piece.get_position())