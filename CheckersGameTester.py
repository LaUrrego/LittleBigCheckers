def get_possible_moves(self, game_board):
    """Returns possible moves for this token"""
    row, column = self._current_position
    possible_moves = []
    if self._type == "Regular":
        # black piece logic
        if self._color == "Black":
            # if row == 0:
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
                        adjacent_candidate.append((row - 1, index))
                # print("adjacent: ", adjacent_candidate)
                two_above = game_board[row - 2]
                for candidates in adjacent_candidate:
                    x_pos, y_pos = candidates
                    # on the right
                    if y_pos > column:
                        if two_above[y_pos + 1] == "OK":
                            possible_moves.append(candidates)
                            possible_moves.append((row - 2, y_pos + 1))
                    # on the left
                    elif y_pos < column:
                        if two_above[y_pos - 1] == "OK":
                            possible_moves.append(candidates)
                            possible_moves.append((row - 2, y_pos - 1))
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
            # if row == 7:
            #   print("BOTTOM EDGE, CHANGE TO KING")
            #    return
            row_below = game_board[row + 1]
            for index, square in enumerate(game_board[row + 1]):
                if square == "OK" and (index == column + 1 or index == column - 1):
                    # add empty space not occupied by enemy or None
                    possible_moves.append((row + 1, index))

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
                    if square == "Black" and index == column + 1 and row < 6:
                        # add candidates
                        adjacent_candidate.append((row + 1, index))
                    if square == "Black" and index == column - 1 and row < 6:
                        adjacent_candidate.append((row + 1, index))
                # print("adjacent: ", adjacent_candidate)
                two_below = game_board[row + 2]
                for candidates in adjacent_candidate:
                    x_pos, y_pos = candidates
                    # on the right
                    if y_pos > column:
                        if two_below[y_pos + 1] == "OK":
                            possible_moves.append(candidates)
                            possible_moves.append((row + 2, y_pos + 1))
                    # on the left
                    elif y_pos < column:
                        if two_below[y_pos - 1] == "OK":
                            possible_moves.append(candidates)
                            possible_moves.append((row + 2, y_pos - 1))
                return possible_moves
            # No black in row above piece
            # else:
            #    for index, square in enumerate(game_board[row + 1]):
            #        if square == "OK" and (index == column + 1 or index == column - 1):
            #            # add empty space not occupied by enemy or None
            #            possible_moves.append((row + 1, index))
            return possible_moves