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
        self._board = new_board

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

class Checkers:
    """
    information about the  board and the players. Board initialized when this object is created.
    """
    def __init__(self):
        # initialized as "Black" for first move
        self._current_turn = "Black"
        self._players = {}
        board = CheckerBoard()
        self.current_board = board.get_board()

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
            pass # continue from here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def get_checker_details(self):
        pass

    def print_board(self):
        """Prints the current game board in the form of an array"""
        pass

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


board = CheckerBoard()

for row in board.get_board():
    print(row)