# Author: Larry Urrego
# Includes a Player and Checkers
# class as well as a Token and CheckerBoard class used to represent changing token pieces and custom board arrangements,
# respectively. Includes a special method for the Checkers class called print_color_board() that takes no arguments and
# prints the current board as a stacked, numbered list of lists with colors utilizing ANSI escape sequences right in the
# terminal for ease of viewing a live display of the board when moving with play_game(). Simple call this method below
# all play_game calls to have it print automatically.
# Game utilizes custom game logic that determines all diagonal pieces of a particular current position (assuming it's
# a valid square and token within play_game), and can indicate if jumps are possible for a given token using
# logic specific for each token type: "Regular", "King", "TripleKing".
# Game initialized with Black as first player per game rules. At any point, for any piece corresponding to a player of
# the current turn, you can use the Checkers method print_moves() to input a (row, column) position and get how many,
# if any, jumps are possible for that piece. Diagonal calculation logic has print-outs that were commented out for
# cleanliness, but can be reimplemented to view a per-move, per-piece print out of moves on each diagonal. Moves are
# displayed as an array of 4 arrays, corresponding to the 4 diagonal sides. Each first element in these arrays goes
# from most adjacent square to edge-most square in that particular diagonal.

class IncorrectColorPieceError(Exception):
    """Custom exception class used to validate player creation with piece color as string 'Black' or 'White'"""
    pass


class OutofTurn(Exception):
    """Custom exception class used to validate player turn, raised when a player attempts to call
    play_game out of turn"""
    pass


class InvalidSquare(Exception):
    """Customer exception class used to validate player move. Raised when a player uses play_game and inputs
    a square location they don't own"""
    pass


class InvalidPlayer(Exception):
    """Custom exception class used to validate player. Raised when a player name is entered in play_game
    that is not one of two recorded players in the game"""
    pass


class ColorsFg:
    """
    Special class utilizing ANSI escape sequences to print color output to the console. Foreground color
    Use as ColorsFg.colorname within a Print statement
    Adapted from: <https://www.geeksforgeeks.org/print-colors-python-terminal/>
    """
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'


class ColorsBg:
    """
    Special class utilizing ANSI escape sequences to print color output to the console. Background color
    Use as ColorsBg.colorname within a Print statement
    Adapted from: <https://www.geeksforgeeks.org/print-colors-python-terminal/>
    """
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    orange = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    lightgrey = '\033[47m'


class Token:
    """Represents a checkers piece token. Can take the form of a regular piece, King or Triple King. Includes
    methods to move it based on official rules"""
    def __init__(self, position, color):
        # can be "Regular", "King" or "TripleKing"
        self._type = "Regular"
        self._current_position = position
        self._color = color

    def get_color(self):
        """
        Get method to return the current token's color

        :return: String
        """
        return self._color

    def change_position(self, position):
        """
        Changes token's current position. Used with game_play during moves

        :param position: Tuple
        :return: Nothing
        """
        self._current_position = position

    def change_type(self, type):
        """
        Changes the current token's type. Input can be "King" or "TripleKing"

        :param type: String
        :return: None
        """
        self._type = type

    def get_position(self):
        """
        Get method to return the current token's position

        :return: Tuple (row, column)
        """
        return self._current_position

    def get_type(self):
        """
        Get method to return the current token's type. Can be: "Regular", "King" or "TripleKing"

        :return: String
        """
        return self._type

    def get_possible_moves(self):
        """
        Returns possible moves for the current token leveraging regular_move_logic and king_move_logic

        :return: Array of arrays
        """
        row, column = self._current_position

        if self._type == "Regular":
            # black piece logic
            if self._color == "Black":
                return self.regular_move_logic("White", row, column)

            # white piece logic
            elif self._color == "White":
                return self.regular_move_logic("Black", row, column)

        elif self._type == "King":
            # black_king piece logic
            if self._color == "Black":
                # can move one forwards or backwards for non capture
                # when possible to capture, can go on any diagonal space as long as only 1 is captured
                # no need for enemies to be adjacent
                return self.king_move_logic("White", row, column)

            # white_king piece logic
            elif self._color == "White":
                return self.king_move_logic("Black", row, column)

        elif self._type == "TripleKing":
            # including "OK" for triple parameter to display all diagonal pieces regardless of color
            if self._color == "Black":
                return self.king_move_logic("White", row, column)
            elif self._color == "White":
                return self.king_move_logic("Black", row, column)

    def regular_move_logic(self, color, row_pos, column_pos):
        """
        Takes the color of the enemy piece, row position, column position
        Returns a list of possible open spaces and identified enemy pieces for used in self.game_play()
        Used only for regular type tokens returns:
        Top 2 diagonals from current position for Black tokens
        Bottom 2 diagonals from current position for White tokens

        :param color: String (foe color)
        :param row_pos: Int
        :param column_pos: Int
        :return: Array of arrays
        """
        diagonal_above_left = []
        diagonal_buffer = [(7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)]
        check = (row_pos, column_pos) in diagonal_buffer

        # current player is black
        if color == "White":
            if row_pos == 0 or check:
                buffer = 1
            else:
                buffer = 0

            for index in range(1, min(row_pos, column_pos) + 1):
                if row_pos - index not in range(8) or column_pos - index not in range(8):
                    pass
                else:
                    diagonal_above_left.append((row_pos - index, column_pos - index))

            #print("from move logic, above left: ",diagonal_above_left)

            diagonal_above_right = []
            for index in range(1, min(row_pos, 8 - column_pos) + buffer):
                if row_pos - index not in range(8) or column_pos + index not in range(8):
                    pass
                else:
                    diagonal_above_right.append((row_pos - index, column_pos + index))

            #print("from move logic, above right:", diagonal_above_right)
            moves = [diagonal_above_left, diagonal_above_right]
            return moves

        # current player is white
        if color == "Black":
            if check:
                buffer = 1
            elif column_pos == 7:
                buffer = 0
            else:
                buffer = 1

            diagonal_bottom_right = []
            for index in range(1, min(8 - row_pos, 8 - column_pos)):
                if row_pos + index not in range(8) or column_pos + index not in range(8):
                    pass
                else:
                    diagonal_bottom_right.append((row_pos + index, column_pos + index))
            #print("from move logic, bottom right: ", diagonal_bottom_right)

            diagonal_bottom_left = []
            for index in range(1, min(8 - row_pos, column_pos) + buffer):
                if row_pos + index not in range(8) or column_pos - index not in range(8):
                    pass
                else:
                    diagonal_bottom_left.append((row_pos + index, column_pos - index))
            #print("from move logic, bottom left: ", diagonal_bottom_left)

            moves = [diagonal_bottom_right, diagonal_bottom_left]
            return moves

    def king_move_logic(self, color, row_pos, column_pos):
        """
        Takes the color of the enemy piece, row position, column position
        Returns a list of possible open spaces and identified enemy pieces for used in self.game_play()
        Returns all available squares in the 4 diagonals of the current position
        Used for King and higher type tokens

        :param color: String (foe color)
        :param row_pos: Int
        :param column_pos: Int
        :return: Array of arrays
        """
        diagonal_buffer = [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (7, 0)]
        check = (row_pos, column_pos) in diagonal_buffer
        if color == "White":
            if row_pos == 0 or check:
                buffer = 1
            else:
                buffer = 0

        # current player is white
        elif color == "Black":
            if check:
                buffer = 1
            elif column_pos == 7:
                buffer = 0
            else:
                buffer = 1

        diagonal_above_left = []
        for index in range(1, min(row_pos, column_pos) + 1):
            if row_pos - index not in range(8) or column_pos - index not in range(8):
                pass
            else:
                diagonal_above_left.append((row_pos - index, column_pos - index))

        #print("from move logic, above left: ",diagonal_above_left)

        diagonal_above_right = []
        for index in range(1, min(row_pos, 8 - column_pos) + buffer):
            if row_pos - index not in range(8) or column_pos + index not in range(8):
                pass
            else:
                diagonal_above_right.append((row_pos - index, column_pos + index))

        #print("from move logic, above right:" ,diagonal_above_right)

        diagonal_bottom_right = []
        for index in range(1, min(8 - row_pos, 8 - column_pos)):
            if row_pos + index not in range(8) or column_pos + index not in range (8):
                pass
            else:
                diagonal_bottom_right.append((row_pos + index, column_pos + index))

        #print("from move logic, bottom right: ", diagonal_bottom_right)

        diagonal_bottom_left = []
        for index in range(1, min(8 - row_pos, column_pos) + buffer):
            if row_pos + index not in range(8) or column_pos - index not in range(8):
                pass
            else:
                diagonal_bottom_left.append((row_pos + index, column_pos - index))

        #print("from move logic, bottom left: ", diagonal_bottom_left)

        moves = [diagonal_above_left, diagonal_bottom_right, diagonal_above_right, diagonal_bottom_left]
        return moves

    def possible_jumps(self, moves_list, board):
        """
        Takes a current position and possible moves list. If a jump is possible, returns > 0 if true
        ,else 0

        :param moves_list: List
        :param board: List of Lists
        :return: Int (0 if no jumps possible, n > 0 for number of jumps possible)
        """
        jumps = 0
        if self._color == "Black":
            foe = "White"
        elif self._color == "White":
            foe = "Black"

        # Translate board rows to strings for evaluation
        for diagonal in moves_list:
            translated_list = []
            if len(diagonal) == 0:
                pass
            for move in diagonal:
                row, column = move
                translated_list.append(board[row][column])
            #print("translated list: ", translated_list)
            if self._type == "King" or self._type == "Regular":
                for space in range(len(translated_list)):
                    if translated_list[space] == "OK":
                        continue
                    elif translated_list[space] != "OK":
                        if self._type == "King":
                            if translated_list[space] != foe:
                                continue
                            elif space < (len(translated_list) - 1) and translated_list[space + 1] == foe:
                                continue
                            elif space < (len(translated_list) - 1) and translated_list[space + 1] == "OK":
                                if translated_list[space - 1] != foe:
                                    jumps += 1
                        if self._type == "Regular":
                            # skip if only 1 move possible
                            if len(translated_list) == 1:
                                pass
                            elif space == 0 and translated_list[space] == foe and translated_list[space + 1] == "OK":
                                jumps += 1

            elif self._type == "TripleKing":
                # Establish enemy piece
                friendly = 0
                opposing = 0
                for square in translated_list:
                    if square == "OK":
                        if opposing == 2:
                            jumps += 1
                        elif opposing == 1:
                            jumps += 1
                        elif opposing > 2:
                            continue
                    elif square == foe:
                        opposing += 1
                    else:
                        friendly += 1
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


class Checkers:
    """
    information about the  board and the players. Board initialized when this object is created.
    position is: (row, column)
    """
    def __init__(self):
        # initialized as "Black" for first move
        self._current_turn = "Black"
        self._players = {}
        self._player_objects = {}
        self._tokens = {
            "Black": [],
            "White": [],
        }
        # Initialize a CheckerBoard to set up the game
        board = CheckerBoard()
        pieces = board.start_setup()
        # fill white pieces
        for item in pieces[0]:
            self._tokens["White"].append(item)
        # fill black pieces
        for item in pieces[1]:
            self._tokens["Black"].append(item)
        self._current_board = board.get_board()

    def get_board_dm(self):
        """
        Get method for testing getting the self._current_board data member for the Checkers class

        :return: Array of arrays
        """
        return self._current_board

    def get_turn(self):
        """
        Get method to display color who's turn it currently is
        :return: "Black" or "White"
        """
        return self._current_turn

    def print_moves(self, position):
        """
        Takes a position tuple (row, column) and used as a testing method to view current
        possible moves by a given token. Only input valid positions for current tokens
        :param position: Tuple (row, column)
        :return: Nothing
        """
        for pieces in self._tokens[self._current_turn]:
            if pieces.get_position() == position:
                moves = pieces.get_possible_moves()
                print("Jumps possible: ", pieces.possible_jumps(moves, self._current_board))

    def remove_token(self, location, foe_color, my_color):
        """
        Method to remove tokens in play during a capture move. Updates player counts when necessary
        :param location: Tuple (row, column)
        :param foe_color: String
        :param my_color: String
        :return: Nothing
        """
        removal_index = 0
        removal_type = ""
        for index, value in enumerate(self._tokens[foe_color]):
            if value.get_position() == location:
                removal_index = index
                if value.get_type() == "King":
                    removal_type = "King"
                elif value.get_type() == "TripeKing":
                    removal_type = "TripleKing"
                break
        self._tokens[foe_color].pop(removal_index)
        row, column = location
        #print("removed: ", location)
        self._current_board[row][column] = "OK"

        # update player's capture count
        self._player_objects[my_color].add_count("Capture")

        # if a king or triple king is captured, update counts
        if removal_type != "":
            self._player_objects[foe_color].remove_count(removal_type)

    def get_white_tokens(self):
        """
        Returns white tokens currently in play

        :return: List
        """
        return self._tokens["White"]

    def get_black_tokens(self):
        """
        Returns black tokens currently in play

        :return: List
        """
        return self._tokens["Black"]

    def setup(self):
        """
        Sets up the board with pieces and fills token collection for each player

        :return: None
        """
        for player in self._tokens:
            for piece in self._tokens[player]:
                x, y = piece.get_position()
                self._current_board[x][y] = piece.get_color()

    def change_turn(self):
        """
        Function to change the current turn's color

        :return: None
        """
        if self._current_turn == "Black":
            self._current_turn = "White"
        elif self._current_turn == "White":
            self._current_turn = "Black"
        return

    def valid_player(self, player_name):
        """
        Checks to see if input name is the currently allowed player to move

        :param player_name: String
        :return: Bool
        """
        if self._players[self._current_turn] == player_name:
            return True
        return False

    def get_square_details(self, position):
        """
        Details on whether the square is None, White, Black, or OK

        :param position: Tuple (row, column)
        :return: String for black square position, None otherwise
        """
        return self._current_board[position[0]][position[1]]

    def get_color(self, name):
        """
        Get method for the color of the player provided as input

        :param name: String
        :return: String
        """
        for key, value in self._players.items():
            if value == name:
                return key

    def valid_square_location(self, position):
        """
        Takes a position and returns true if square coordinates are valid, false if None, or raises InvalidSquare
        if not valid
        :param position: Tuple (row, column)
        :return: Bool
        """
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
        """
        Creates a player given a name and piece color. Raises a IncorrectColorPieceError
         if anything other than "Black" or "White" is given as input. Uses data validation
         to accept any case for black or white.
         Returns a Player object

        :param player_name: String
        :param piece_color: String ("Black" or "White")
        :return: Player object
        """
        if piece_color.lower() == "black":
            self._players["Black"] = player_name
            new_player = Player(player_name,"Black")
            self._player_objects["Black"] = new_player
            return new_player
        elif piece_color.lower() == "white":
            self._players["White"] = player_name
            new_player = Player(player_name, "White")
            self._player_objects["White"] = new_player
            return new_player
        else:
            raise IncorrectColorPieceError("Piece color can only be 'White' or 'Black'!")

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        Main game logic method taking a player name, starting square and ending square
        location and corresponds to a single “move” play. Exceptions handled by:
        Raising OutofTurn exception for moves made by player other than currently allowed
        Raising InvalidSquare if a square outside the board or an illegal (white square) is given
        Also raising InvalidSquare if current player does not own the token position entered
        Raising InvalidPlayer if not player_name doesn't correspond to one of two recorded
        Finds the Token object corresponding to starting location and uses get_possible_moves in
        combination with possible_jumps to identify if the turn has ended. If no capture is possible,
        changes turn at the end of the call. If a piece moves to the opposite end of its respective side,
        it changes the token’s type to “King”. If Token is of type “King” and it reaches
        it’s original side’s starting row, it changes to type “TripleKing”.
        Uses change_location to move.
        Assumes that players will move according to the rules and prioritize a capture move if it’s possible

        :param player_name: String, needs to correspond to a valid player in self._players
        :param starting_square_location: Tuple (row, column), needs to be the location of a valid Token
                                            object belonging to the current player
        :param destination_square_location: Tuple (row,column), needs to be within bounds of the board
                                            and correspond to an empty, valid square space legal for movement
        :return: Int: Number of enemy pieces captured ( n >= 0)
        """
        if player_name not in self._players.values():
            raise InvalidPlayer("This is not a valid player!")
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

            # starting_square_location should match one of the current pieces in play
            for tokens in self._tokens[self._current_turn]:
                if tokens.get_position() == starting_square_location:

                    #print("Pre-Move_______")
                    moves = tokens.get_possible_moves()

                    # test to translate moves visually
                    #print("Post-Move______")
                    captures = 0
                    if self._current_turn == "Black":
                        foe = "White"
                    elif self._current_turn == "White":
                        foe = "Black"

                    for diagonal in moves:
                        # find the relevant move list
                        if destination_square_location not in diagonal:
                            pass
                        elif destination_square_location in diagonal:
                            translated_list = []
                            index = 0
                            for square in range(len(diagonal)):
                                if diagonal[square] != destination_square_location:
                                    continue
                                else:
                                    # index position of the selection destination within the moves list
                                    index = square

                            if tokens.get_type() == "Regular":
                                # found the destination, and it's not the first of the list, indicating capture
                                if index > 0:
                                    # since it needs to be adjacent and only 1 before
                                    captured_piece = diagonal[index - 1]
                                    tokens.change_position(destination_square_location)
                                    # remove the capture piece from the board
                                    self.remove_token(captured_piece, foe, self._current_turn)
                                    # increase capture count
                                    captures += 1

                                # found destination, not a capture move
                                elif index == 0:
                                    # change current position
                                    tokens.change_position(destination_square_location)

                                # update old position with empty space available
                                x,y = starting_square_location
                                self._current_board[x][y] = "OK"

                                # now check if promotion
                                if self._current_turn == "Black":
                                    if tokens.get_position()[0] == 0:
                                        tokens.change_type("King")
                                        # add to player's count
                                        self._player_objects["Black"].add_count("King")
                                if self._current_turn == "White":
                                    if tokens.get_position()[0] == 7:
                                        tokens.change_type("King")
                                        # add to player's count
                                        self._player_objects["White"].add_count("King")

                                # refresh board by updating from piece object locations
                                self.setup()

                                # redefine moves for new position
                                moves = tokens.get_possible_moves()

                                # non capture move
                                if tokens.get_type() == "Regular":
                                    if captures == 0:
                                        self.change_turn()
                                    else:
                                        # capture move, but no jumps available
                                        if tokens.possible_jumps(moves, self._current_board) == 0:
                                            self.change_turn()

                                    return captures
                                elif tokens.get_type() == "King":
                                    if tokens.possible_jumps(moves, self._current_board) == 0:
                                        self.change_turn()
                                    return captures

                            elif tokens.get_type() == "King" or tokens.get_type() == "TripleKing":
                                # moving adjacent, not a capture/jump move:
                                if index == 0:
                                    tokens.change_position(destination_square_location)

                                # Jump was made
                                elif index > 0:
                                    jumped_pieces = diagonal[:index]
                                    for position in range(len(jumped_pieces)):
                                        current = jumped_pieces[position]
                                        # coordinate locations of current piece in list
                                        cur_x, cur_y = current
                                        board_square = self._current_board[cur_x][cur_y]
                                        # update position
                                        tokens.change_position(destination_square_location)
                                        # skip open space since a king can jump any to capture
                                        # when used with a TripleKing, skip friendlies as well
                                        if board_square == "OK" or board_square == self._current_turn:
                                            continue
                                        elif board_square == foe:
                                            # clear it from the board
                                            self._current_board[cur_x][cur_y] = "OK"
                                            # remove from play
                                            self.remove_token(current, foe, self._current_turn)
                                            captures += 1

                                # update old position with empty space available
                                x, y = starting_square_location
                                self._current_board[x][y] = "OK"

                                # now check if promotion
                                if tokens.get_type() == "King":
                                    if self._current_turn == "Black":
                                        if tokens.get_position()[0] == 7:
                                            tokens.change_type("TripleKing")
                                            # add to player's count
                                            self._player_objects["Black"].add_count("TripleKing")
                                            # remove the old count
                                            self._player_objects["Black"].remove_count("King")
                                    if self._current_turn == "White":
                                        if tokens.get_position()[0] == 0:
                                            tokens.change_type("TripleKing")
                                            # add to player's count
                                            self._player_objects["White"].add_count("TripleKing")
                                            # remove the old count
                                            self._player_objects["White"].remove_count("King")

                                # refresh board by updating from piece object locations
                                self.setup()

                                # redefine moves for new position
                                moves = tokens.get_possible_moves()

                                # non capture move
                                if tokens.possible_jumps(moves, self._current_board) != 0:
                                    if captures == 0:
                                        # jumps possible but wasn't a jump move prior
                                        self.change_turn()
                                        return captures
                                    elif captures > 0:
                                        # don't switch turns with jumps possible after a capture move
                                        return captures
                                # no jumps possible
                                elif tokens.possible_jumps(moves, self._current_board) == 0:
                                    self.change_turn()
                                    return captures

    def get_checker_details(self, square_location):
        """
        Takes a position on the board and returns the type of token currently on it or None if empty
        Raises InvalidSquare exception if the location tuple is outside the bounds of the board.

        :param square_location: Tuple (row, column)
        :return: String or None
        """
        row, column = square_location
        if row not in range(8) or column not in range(8):
            raise InvalidSquare("Not a valid square location!")

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
        """
        Prints the current game board in the form of an array

        :return: Array of arrays
        """
        # update self._current_board with current positions, for posterity
        self.setup()
        board_array = []
        for row in range(len(self._current_board)):
            new_row = []
            for square in range(len(self._current_board[row])):
                if self.get_checker_details((row,square)) is None:
                    new_row.append("None")
                else:
                    new_row.append(self.get_checker_details((row,square)))
            board_array.append(new_row)
        return board_array

    def print_color_board(self):
        """
        Uses ANSI escape codes in classes ColorsFg and ColorsBg to print a colored, stacked representation
        of the Array of arrays checkerboard, with numbered rows and columns

        :return: None, printed to console
        """
        row_num = 0
        print("    0    1    2    3    4    5    6    7")
        for row in range(8):
            print(row_num, end=" ")
            row_num += 1
            for piece in range(8):
                current = self._current_board[row][piece]
                if current == "White":
                    for token in self._tokens["White"]:
                        if token.get_position() == (row, piece):
                            piece_type = token.get_type()
                            break
                    if piece_type == "Regular":
                        display = "W"
                    elif piece_type == "King":
                        display = "K"
                    elif piece_type == "TripleKing":
                        display = "T"
                    print(ColorsBg.black, ColorsFg.lightgrey, display, ' \x1b[0m', end="")
                elif current == "Black":
                    for token in self._tokens["Black"]:
                        if token.get_position() == (row, piece):
                            piece_type = token.get_type()
                            break
                    if piece_type == "Regular":
                        display = "B"
                    elif piece_type == "King":
                        display = "K"
                    elif piece_type == "TripleKing":
                        display = "T"
                    print(ColorsBg.black, ColorsFg.cyan, display, ' \x1b[0m', end="")
                elif current == "OK":
                    print(ColorsBg.black, ColorsFg.lightgrey, " ", ' \x1b[0m', end="")
                elif current is None:
                    print(ColorsBg.lightgrey, "  ", ' \x1b[0m', end="")
            print("")
        print("    0    1    2    3    4    5    6    7")

    def game_winner(self):
        """
        If the game has not ended returns 'Game has not ended', otherwise returns the name of the winner
        Utilizes the amount of tokens currently in play (len == 0 is the loser) to determine winner

        :return: String
        """
        black_count = len(self._tokens["Black"])
        white_count = len(self._tokens["Black"])

        if black_count == 0:
            return self._players["White"]
        elif white_count == 0:
            return self._players["Black"]
        else:
            return "Game has not ended"


class Player:
    """Simulates a player in checkers, initialized with a player_name and checker_color. Includes methods to return
    the color, capture count, number of king pieces, and number of triple king pieces"""
    def __init__(self, player_name, checker_color):
        self._player_name = player_name
        self._checker_color = checker_color
        self._king_count = 0
        self._triple_king_count = 0
        self._capture_count = 0

    def get_name(self):
        """
        Get method to get the current Player object's name

        :return: String
        """
        return self._player_name

    def add_count(self, count_type):
        """
        General method for adding count to a player's data member records.
        Utilizes the following identify strings:
        self._king_count - modified with 'King'
        self._triple_king_count - modified with 'TripleKing'
        self._capture_count - modified with 'Capture'
        otherwise raises an AttributeError for any other string entered

        :param count_type: String
        :return: None
        """
        if count_type == "King":
            self._king_count += 1
        elif count_type == "TripleKing":
            self._triple_king_count += 1
        elif count_type == "Capture":
            self._capture_count += 1
        else:
            raise AttributeError("Not an accepted type!")

    def remove_count(self, count_type):
        """
        Method to remove kings and triple kings from a player's count when they're captured
        raises an AttributeError if any other string is passed instead
        Accepts "King" or "TripleKing" as input

        :param count_type: String
        :return: None
        """
        if count_type == "King":
            self._king_count -= 1
        elif count_type == "TripleKing":
            self._triple_king_count -= 1
        else:
            raise AttributeError("Not an accepted type!")

    def get_checker_color(self):
        """
        Returns the players checker color

        :return: String
        """
        return self._checker_color

    def get_king_count(self):
        """
        Returns the number of kings this player has

        :return: Int
        """
        return self._king_count

    def get_triple_king_count(self):
        """
        Returns the number of triple kings this player has

        :return: Int
        """
        return self._triple_king_count

    def get_captured_pieces_count(self):
        """
        Returns the amount of captures pieces by the current player

        :return: Int
        """
        return self._capture_count







