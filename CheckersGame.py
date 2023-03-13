# Author: Larry Urrego
# GitHub username: LaUrrego
# Date:
# Description: Checkers simulator...
import ColorFile

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


class Token:
    """Represents a checkers piece token. Can take the form of a regular piece, King or Triple King. Includes
    methods to move it based on official rules"""
    def __init__(self, position, color):
        # can be "Regular", "King" or "TripleKing"
        self._type = "Regular"
        self._current_position = position
        self._color = color

    def get_color(self):
        return self._color

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
        diagonal_above_left = []
        diagonal_buffer = [(7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)]
        check = (row_pos, column_pos) in diagonal_buffer

        # current player is black
        if color == "White":
            if row_pos == 0 or check:
                buffer = 1
            else:
                buffer = 0
        # account for corner (7,0) or (0,7)
        #if (row_pos == 7 and column_pos == 0) or (row_pos == 0 and column_pos == 7):
            for index in range(1, min(row_pos, column_pos) + 1):
                if row_pos - index not in range(8) or column_pos - index not in range(8):
                    pass
                else:
                    diagonal_above_left.append((row_pos - index, column_pos - index))

            print("from move logic, above left: ",diagonal_above_left)

            diagonal_above_right = []
            for index in range(1, min(row_pos, 8 - column_pos) + buffer):
                if row_pos - index not in range(8) or column_pos + index not in range(8):
                    pass
                else:
                    diagonal_above_right.append((row_pos - index, column_pos + index))

            print("from move logic, above right:", diagonal_above_right)
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
            print("from move logic, bottom right: ", diagonal_bottom_right)

            diagonal_bottom_left = []
            for index in range(1, min(8 - row_pos, column_pos) + buffer):
                if row_pos + index not in range(8) or column_pos - index not in range(8):
                    pass
                else:
                    diagonal_bottom_left.append((row_pos + index, column_pos - index))
            print("from move logic, bottom left: ", diagonal_bottom_left)

            moves = [diagonal_bottom_right, diagonal_bottom_left]
            return moves

    def king_move_logic(self, color, row_pos, column_pos):
        """Takes a color of the enemy piece, row position, column position and current game board
        Returns a list of possible open spaces and identified enemy pieces for used in self.game_play()
        default parameter 'triple' initialized as None for King logic, but when changed to 'OK' allows for
        use with Triple King by returning all available diagonal squares regardless of color """
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
                #current = board[row_pos - index][column_pos - index]
                #if triple is None:
                #    if current == "OK" or current == color:
                #        diagonal_above_left.append((row_pos - index, column_pos - index))
                #elif triple == "OK":
                #    diagonal_above_left.append((row_pos - index, column_pos - index))
        print("from move logic, above left: ",diagonal_above_left)

        diagonal_above_right = []
        for index in range(1, min(row_pos, 8 - column_pos) + buffer):
            if row_pos - index not in range(8) or column_pos + index not in range(8):
                pass
            else:
                diagonal_above_right.append((row_pos - index, column_pos + index))
                #current = board[row_pos - index][column_pos + index]
                #if triple is None:
                #    if current == "OK" or current == color:
                #        diagonal_above_right.append((row_pos - index, column_pos + index))
                #elif triple == "OK":
                #    diagonal_above_right.append((row_pos - index, column_pos + index))
        print("from move logic, above right:" ,diagonal_above_right)

        diagonal_bottom_right = []
        for index in range(1, min(8 - row_pos, 8 - column_pos)):
            if row_pos + index not in range(8) or column_pos + index not in range (8):
                pass
            else:
                diagonal_bottom_right.append((row_pos + index, column_pos + index))
                #current = board[row_pos + index][column_pos + index]
                #if triple is None:
                #    if current == "OK" or current == color:
                #        diagonal_bottom_right.append((row_pos + index, column_pos + index))
                #elif triple == "OK":
                #    diagonal_bottom_right.append((row_pos + index, column_pos + index))
        print("from move logic, bottom right: ", diagonal_bottom_right)

        diagonal_bottom_left = []
        for index in range(1, min(8 - row_pos, column_pos) + buffer):
            if row_pos + index not in range(8) or column_pos - index not in range(8):
                pass
            else:
                diagonal_bottom_left.append((row_pos + index, column_pos - index))
                #current = board[row_pos + index][column_pos - index]
                #if triple is None:
                #    if current == "OK" or current == color:
                #        diagonal_bottom_left.append((row_pos + index, column_pos - index))
                #elif triple == "OK":
                #    diagonal_bottom_left.append((row_pos + index, column_pos - index))
        print("from move logic, bottom left: ", diagonal_bottom_left)

        moves = [diagonal_above_left, diagonal_bottom_right, diagonal_above_right, diagonal_bottom_left]
        return moves

    def possible_jumps(self, moves_list, board):
        """Takes a current position and possible moves list. If a jump is possible, returns > 0 if true
        ,else 0"""
        jumps = 0
        if self._color == "Black":
            foe = "White"
        elif self._color == "White":
            foe = "Black"
        for diagonal in moves_list:
            translated_list = []
            if len(diagonal) == 0:
                pass
            for move in diagonal:
                row, column = move
                translated_list.append(board[row][column])
            print("translated list: ", translated_list)
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
        self._player_objects = {}
        self._tokens = {
            "Black": [],
            "White": [],
        }
        #self._current_board = None
        board = CheckerBoard()
        pieces = board.start_setup()
        # fill white pieces
        for item in pieces[0]:
            self._tokens["White"].append(item)
        # fill black pieces
        for item in pieces[1]:
            self._tokens["Black"].append(item)
        self._current_board = board.get_board()

    def get_turn(self):
        return self._current_turn

    def print_moves(self, position):
        for pieces in self._tokens[self._current_turn]:
            if pieces.get_position() == position:
                moves = pieces.get_possible_moves(self._current_board)
                print("Jumps possible: ", pieces.possible_jumps(moves, self._current_board))

    def remove_token(self, location, foe_color, my_color):
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
        row,column = location
        print("removed: ", location)
        self._current_board[row][column] = "OK"
        # update player's capture count
        self._player_objects[my_color].add_count("Capture")
        # if a king or triple king is captured, update counts
        if removal_type != "":
            self._player_objects[foe_color].remove_count(removal_type)
        #print("Added to captured")

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
        for player in self._tokens:
            for piece in self._tokens[player]:
                x, y = piece.get_position()
                self._current_board[x][y] = piece.get_color()


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
        """Nie Wiem"""
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
            #if player_name not in self._players.values():
            #    raise InvalidPlayer("This is not a valid player!")
            # should match one of the current pieces in play
            for tokens in self._tokens[self._current_turn]:
                if tokens.get_position() == starting_square_location:

                    #print("Pre-Move___________________________________________________________________")
                    moves = tokens.get_possible_moves(self._current_board)

                    # test to translate moves visually

                    print("Post-Move__________________________________________________________________")
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
                                moves = tokens.get_possible_moves(self._current_board)

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
                                moves = tokens.get_possible_moves(self._current_board)

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
        self.setup()
        return self._current_board

    def game_winner(self):
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

    def add_count(self, count_type):
        """General method for adding count to a player's data member records.
        Utilizes the following identify strings:
        self._king_count - modified with 'King'
        self._triple_king_count - modified with 'TripleKing'
        self._capture_count - modified with 'Capture"
        otherwise raises an AttributeError for any other string entered
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
        """Method to remove kings and triple kings from a player's count when they're captured"""
        if count_type == "King":
            self._king_count -= 1
        elif count_type == "TripleKing":
            self._triple_king_count -= 1
        else:
            raise AttributeError("Not an accepted type!")

    def get_checker_color(self):
        """Returns the players checker color"""
        return self._checker_color

    def get_king_count(self):
        """Returns the number of kings this player has"""
        return self._king_count

    def get_triple_king_count(self):
        """Returns the number of triple kings this player has"""
        return self._triple_king_count

    def get_captured_pieces_count(self):
        """Returns the amount of captures pieces by the current player"""
        return self._capture_count



game = Checkers()
Larry = game.create_player("Larry", "black")
Karolcia = game.create_player("Karolcia", "white")
#game.test_adder("White", (4,5))
#game.test_adder("White", (4,3))
#game.test_color_change("White")

game.play_game("Larry", (5,4), (4,5))
game.play_game("Karolcia", (2,5), (3,4))
game.play_game("Larry", (5,2),(4,1))
game.play_game("Karolcia", (2,1),(3,0))
game.play_game("Larry",(5,6), (4,7))
game.play_game("Karolcia",(3,0),(5,2))
game.play_game("Larry",(6,1),(4,3))
game.play_game("Larry", (4,3), (2,5))
game.play_game("Karolcia",(1,4), (3,6))
game.play_game("Karolcia",(3,6),(5,4))
game.play_game("Larry",(6,3),(4,5))
game.play_game("Karolcia",(2,3),(3,2))
game.play_game("Larry", (7,2),(6,3))
game.play_game("Karolcia", (1,2), (2,3))
game.play_game("Larry", (5,0),(4,1))
game.play_game("Karolcia", (3,2),(5,0))
game.play_game("Larry",(4,7),(3,6))
game.play_game("Karolcia",(5,0),(6,1))
game.play_game("Larry", (3,6),(2,5))
game.play_game("Karolcia", (6,1),(7,2))
game.play_game("Karolcia",(7,2),(5,4))
game.play_game("Karolcia",(5,4), (3,6))
game.play_game("Karolcia", (3,6),(1,4))
game.play_game("Larry", (6,7),(5,6))
game.play_game("Karolcia", (2,3), (3,2))
game.play_game("Larry", (6,5),(5,4))
game.play_game("Karolcia", (1,4), (2,3))
game.play_game("Larry", (7,0), (6,1))
game.play_game("Karolcia",(2,3),(6,7))
game.play_game("Larry",(5,4),(4,5))
game.play_game("Karolcia",(6,7),(1,2))
game.play_game("Larry",(6,1),(5,2))
game.play_game("Karolcia",(1,0),(2,1))
game.play_game("Larry",(5,2),(4,3))
game.play_game("Karolcia", (0,1),(1,0))
game.play_game("Larry",(4,3), (3,4))
game.play_game("Karolcia",(1,2),(0,1))
game.play_game("Larry",(3,4),(2,3))
game.play_game("Karolcia",(0,3),(1,2))
game.play_game("Larry",(7,6),(6,5))
game.play_game("Karolcia",(3,2),(4,1))
game.play_game("Larry",(2,3), (1,4))
game.play_game("Karolcia", (0,1),(3,4))
game.play_game("Larry",(1,4),(0,3))
game.play_game("Karolcia", (2,1),(3,0))
game.play_game("Larry",(0,3),(2,1))
game.play_game("Karolcia",(1,0),(3,2))
game.play_game("Larry",(6,5),(5,6))
game.play_game("Karolcia",(3,4),(6,7))
game.play_game("Larry", (7,4),(6,3))
game.play_game("Karolcia",(4,1),(5,2))
game.play_game("Larry",(6,3),(4,1))
game.play_game("Larry",(4,1),(2,3))
game.play_game("Karolcia",(6,7),(0,1))
print("BOTTOM-------------------------------------------------------------")
game.print_moves((0,3))
print("current turn after move:", game.get_turn())
print("captured pieces Larry: ", Larry.get_captured_pieces_count())
print("captured pieces Karolcia: ", Karolcia.get_captured_pieces_count())
#for token in game._tokens["White"]:
#    if token.get_position() == (7,2):
#        print(token.get_type())
row_num = 0
print("    0    1    2    3    4    5    6    7")
for row in range(8):
    print(row_num, end=" ")
    row_num += 1
    for piece in range(8):
        current = game._current_board[row][piece]
        if current == "White":
            for token in game._tokens["White"]:
                if token.get_position() == (row,piece):
                    piece_type = token.get_type()
                    break
            if piece_type == "Regular":
                display = "W"
            elif piece_type == "King":
                display = "K"
            elif piece_type == "TripleKing":
                display = "T"
            print(ColorFile.bg.black, ColorFile.fg.lightgrey, display, ' \x1b[0m', end="")
        elif current == "Black":
            for token in game._tokens["Black"]:
                if token.get_position() == (row,piece):
                    piece_type = token.get_type()
                    break
            if piece_type == "Regular":
                display = "B"
            elif piece_type == "King":
                display = "K"
            elif piece_type == "TripleKing":
                display = "T"
            print(ColorFile.bg.black, ColorFile.fg.cyan, display, ' \x1b[0m', end="")
        elif current == "OK":
            print(ColorFile.bg.black, ColorFile.fg.lightgrey, " ", ' \x1b[0m', end="")
        elif current is None:
            print(ColorFile.bg.lightgrey, "  ", ' \x1b[0m', end="")
    print("")
print("    0    1    2    3    4    5    6    7")

if game.game_winner() == "Game has not ended":
    print("Game has not ended")
else:
    print("The winner is: ", game.game_winner())

print("Larry counts: ")
print("kings: ", Larry.get_king_count())
print("Triple Kings: ", Larry.get_triple_king_count())
print("Karolcia counts: ")
print("kings: ", Karolcia.get_king_count())
print("Triple Kings: ", Karolcia.get_triple_king_count())
