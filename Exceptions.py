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