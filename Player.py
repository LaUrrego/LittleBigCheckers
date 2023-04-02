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