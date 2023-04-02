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

