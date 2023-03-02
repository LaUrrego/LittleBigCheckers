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


class Checkers:
    """
    information about the  board and the players. Board initialized when this object is created.
    """
    def __init__(self):
        pass

    def create_player(self, player_name, piece_color):
        if piece_color.lower() == "black" or piece_color.lower() == "white":
            return Player(player_name, piece_color)
        else:
            raise IncorrectColorPieceError("Piece color can only be 'White' or 'Black'!")

    def play_game(self, player_name, starting_square_location, destination_square_location):
        pass

    def get_checker_details(self):
        pass

    def print_board(self):
        """Prints the current game board in the form of an array"""
        board = []
        for row in range(8):
            if row % 2 == 0:
                whole_row = []
                for column in range(8):
                    if column % 2 == 0:
                        whole_row.append(None)
                    else:
                        whole_row.append("White")
                board.append(whole_row)
            else:
                whole_row = []
                for column in range(8):
                    if column % 2 == 0:
                        whole_row.append("White")
                    else:
                        whole_row.append(None)
                board.append(whole_row)
        return board

    def game_winner(self):
        pass


class Player:

    def __init__(self, player_name, checker_color):
        self._player_name = player_name
        self._checker_color = checker_color

    def get_king_count(self):
        pass

    def get_triple_king_count(self):
        pass

    def get_captured_pieces_count(self):
        pass


game = Checkers()

for row in game.print_board():
    print(row)