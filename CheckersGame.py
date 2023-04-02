import os
from CheckerBoard import CheckerBoard
from Colors import ColorsBg, ColorsFg
from Exceptions import IncorrectColorPieceError, OutofTurn, InvalidSquare, InvalidPlayer
from Player import Player


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
        white_count = len(self._tokens["White"])

        if black_count == 0:
            return self._players["White"]
        elif white_count == 0:
            return self._players["Black"]
        else:
            return "Game has not ended"

    def input_translate(self, move_string: str):
        """
        Translates a user-input move into a usable tuple form to play
        :param move_string: String
        :return: Tuple
        """
        num_only = move_string.strip("() ,")
        row = int(num_only[0])
        column = int(num_only[-1])
        return row, column


if __name__ == "__main__":
    # clear screen
    os.system('clear')

    game = Checkers()
    player1_name = input("Enter a name for player 1: ")
    player1_color = input("Enter your color (Black or White): ")
    player2_name = input("Enter a name for player 2: ")
    player2_color = input("Enter your color (Black or White, can not be same as player 1): ")
    player1 = game.create_player(player1_name, player1_color)
    player2 = game.create_player(player2_name, player2_color)

    while game.game_winner() == "Game has not ended":
        # clear screen
        os.system('clear')

        if game.get_turn() == player1.get_checker_color():
            current_player = player1.get_name()
        else:
            current_player = player2.get_name()
        print("=====================================")
        print("Current player is: ", game.get_turn())
        print("Player 1: ", player1_name, "|", player1_color)
        print("Captured: ", player1.get_captured_pieces_count())
        print("Player 2: ", player2_name, "|", player2_color)
        print("Captured: ", player2.get_captured_pieces_count())
        print("=====================================")

        # display board
        game.print_color_board()

        check = input("What to check possible jumps? (y/n)")
        if check.lower() == "y":
            position = game.input_translate(input("Which piece should we check? (row, column): "))
            game.print_moves(position)

        start_move = game.input_translate(input("What is your next move?\n   Which piece to start? (row, column): "))
        destination_move = game.input_translate(input("   Where are you moving it to? (row, column): "))
        game.play_game(current_player, start_move, destination_move)

    print(game.game_winner())