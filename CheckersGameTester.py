import unittest
from CheckersGame import Token, CheckerBoard, Checkers, Player, ColorsFg, ColorsBg, \
    IncorrectColorPieceError, OutofTurn, InvalidSquare, InvalidPlayer


class TokenTest(unittest.TestCase):
    def test_token_init(self):
        token1 = Token((2, 1), "Black")
        token2 = Token((3, 4), "White")

        self.assertEqual(token1.get_color(), "Black")
        self.assertEqual(token1.get_position(), (2, 1))
        self.assertEqual(token1.get_type(), "Regular")
        self.assertEqual(token2.get_color(), "White")

    def test_change_position(self):
        token1 = Token((2, 1), "Black")
        token1.change_position((3, 2))

        self.assertEqual(token1.get_position(), (3, 2))

    def test_change_type(self):
        token1 = Token((2, 1), "Black")
        token1.change_type("King")

        self.assertEqual(token1.get_type(), "King")

    def test_regular_move_logic(self):
        token1 = Token((5, 2), "Black")
        token2 = Token((5, 6), "White")
        moves1 = token1.regular_move_logic("White", 5, 2)
        moves2 = token2.regular_move_logic("Black", 5, 6)

        self.assertIn([(4, 1), (3, 0)], moves1)
        self.assertIn([(6, 5), (7, 4)], moves2)

    def test_king_move_logic(self):
        token1 = Token((5, 4), "Black")
        token1.change_type("King")
        moves1 = token1.king_move_logic("White", 5, 4)

        self.assertIn([(4, 5), (3, 6), (2, 7)], moves1)

    def test_get_possible_moves(self):
        token1 = Token((5, 4), "Black")
        token1.change_type("TripleKing")
        moves1 = token1.get_possible_moves()

        self.assertIn([(4, 3), (3, 2), (2, 1), (1, 0)], moves1)

    def test_possible_jumps(self):
        game = Checkers()
        player1 = game.create_player("A", "black")
        player2 = game.create_player("B", "white")

        game.play_game("A", (5, 4), (4, 5))
        game.play_game("B", (2, 5), (3, 4))
        game.play_game("A", (4, 5), (3, 6))
        white_pieces = game.get_white_tokens()
        for token in white_pieces:
            if token.get_position() == (2, 7):
                moves = token.get_possible_moves()
                board = game.get_board_dm()
                jumps = token.possible_jumps(moves, board)

        self.assertEqual(jumps, 1)


class CheckerBoardTest(unittest.TestCase):

    def test_board_filler(self):

        test_board = [
            [None, "OK", None, "OK", None, "OK", None, "OK"],
            ["OK", None, "OK", None, "OK", None, "OK", None],
            [None, "OK", None, "OK", None, "OK", None, "OK"],
            ["OK", None, "OK", None, "OK", None, "OK", None],
            [None, "OK", None, "OK", None, "OK", None, "OK"],
            ["OK", None, "OK", None, "OK", None, "OK", None],
            [None, "OK", None, "OK", None, "OK", None, "OK"],
            ["OK", None, "OK", None, "OK", None, "OK", None],
        ]

        board = CheckerBoard()

        self.assertEqual(board.get_board(), test_board)

    def test_filler(self):

        test_board = [
            ["A", "B", "A", "B", "A", "B", "A", "B"],
            ["B", "A", "B", "A", "B", "A", "B", "A"],
            ["A", "B", "A", "B", "A", "B", "A", "B"],
            ["B", "A", "B", "A", "B", "A", "B", "A"],
            ["A", "B", "A", "B", "A", "B", "A", "B"],
            ["B", "A", "B", "A", "B", "A", "B", "A"],
            ["A", "B", "A", "B", "A", "B", "A", "B"],
            ["B", "A", "B", "A", "B", "A", "B", "A"],
        ]

        board = CheckerBoard()

        self.assertEqual(board.filler("B", "A"), test_board)


class PlayerTest(unittest.TestCase):

    def test_player_init(self):
        player1 = Player("Jack", "White")

        self.assertEqual(player1.get_checker_color(), "White")
        self.assertEqual(player1.get_captured_pieces_count(), 0)
        self.assertEqual(player1.get_king_count(), 0)
        self.assertEqual(player1.get_triple_king_count(), 0)
        self.assertNotEqual(player1.get_name(), "Steve")
        self.assertEqual(player1.get_name(), "Jack")

    def test_player_counts(self):
        player1 = Player("Larry", "Black")

        player1.add_count("Capture")
        player1.add_count("King")
        player1.add_count("TripleKing")
        player1.add_count("TripleKing")
        player1.add_count("TripleKing")
        player1.add_count("King")
        player1.add_count("King")
        player1.add_count("King")
        player1.remove_count("King")

        self.assertEqual(player1.get_king_count(), 3)
        self.assertEqual(player1.get_captured_pieces_count(), 1)
        self.assertEqual(player1.get_triple_king_count(), 3)


class ColorsFgTest(unittest.TestCase):

    def test_fg_color(self):
        self.assertEqual(ColorsFg.black, '\033[30m')
        self.assertEqual(ColorsFg.lightcyan, '\033[96m')


class ColorsBgTest(unittest.TestCase):

    def test_bg_color(self):
        self.assertEqual(ColorsBg.black, '\033[40m')
        self.assertEqual(ColorsBg.green, '\033[42m')


class CheckersTest(unittest.TestCase):

    def test_checkers_init(self):
        game = Checkers()
        white_piece_objects = game.get_white_tokens()
        white_token_pos = [token.get_position() for token in white_piece_objects]
        black_pieces_objects = game.get_black_tokens()
        black_token_pos = [token.get_position() for token in black_pieces_objects]

        self.assertEqual(game.get_turn(), "Black")
        self.assertIn((0, 1), white_token_pos)
        self.assertIn((5, 4), black_token_pos)

    def test_create_player(self):
        game = Checkers()
        player1 = game.create_player("John", "WhiTe")
        player2 = game.create_player("Peter", "bLaCk")

        self.assertEqual(player1.get_checker_color(), "White")
        self.assertEqual(player2.get_checker_color(), "Black")
        self.assertTrue(game.valid_player("Peter"))
        self.assertFalse(game.valid_player("John"))
        self.assertTrue(game.valid_square_location((1, 0)))
        self.assertRaises(InvalidSquare, game.valid_square_location, (9, 9))
        self.assertRaises(IncorrectColorPieceError, game.create_player, "Bob", "Red")

    def test_play_game(self):
        game = Checkers()
        player1 = game.create_player("Paul", "White")
        player2 = game.create_player("Jackie", "Black")

        self.assertRaises(InvalidPlayer, game.play_game, "Steve", (0, 1), (0, 0))
        self.assertRaises(OutofTurn, game.play_game, "Paul", (0, 1), (0, 0))

        game.play_game("Jackie", (5, 4), (4, 5))
        game.play_game("Paul", (2, 5), (3, 4))
        game.play_game("Jackie", (4, 5), (3, 6))
        capture = game.play_game("Paul", (2, 7), (4, 5))

        self.assertEqual(capture, 1)

        game.play_game("Jackie", (5, 6), (4, 7))
        game.play_game("Paul", (4, 5), (5, 4))
        game.play_game("Jackie", (6, 5), (5, 6))
        game.play_game("Paul", (5, 4), (6, 5))
        game.play_game("Jackie", (5, 6), (4, 5))
        game.play_game("Paul", (3, 4), (4, 3))
        game.play_game("Jackie", (6, 7), (5, 6))
        game.play_game("Paul", (4, 3), (5, 4))
        game.play_game("Jackie", (7, 6), (6, 7))

        white_token_objects = game.get_white_tokens()
        test_type = ""
        for token in white_token_objects:
            if token.get_position() == (6, 5):
                test_type = token.get_type()
            else:
                pass

        self.assertEqual(test_type, "Regular")

        captures2 = game.play_game("Paul", (6, 5), (7, 6))

        self.assertEqual(captures2, 0)

        for token in white_token_objects:
            if token.get_position() == (7, 6):
                test_type = token.get_type()
            else:
                pass
        self.assertEqual(test_type, "King")
        self.assertEqual(game.get_checker_details((7, 6)), "White_king")
        self.assertIsNone(game.get_checker_details((0, 0)))
        self.assertEqual(game.get_checker_details((4, 5)), "Black")

        self.assertEqual(player1.get_king_count(), 1)

        game.remove_token((7,6), "White", "Black")

        self.assertEqual(player1.get_king_count(), 0)
        self.assertIsNone(game.get_checker_details((7, 6)))

    def test_game_winner(self):
        game = Checkers()
        player1 = game.create_player("Bob", "White")
        player2 = game.create_player("Booth", "Black")

        game.play_game("Booth", (5, 4), (4, 5))
        game.play_game("Bob", (2, 5), (3, 4))
        game.play_game("Booth", (4, 5), (3, 6))
        game.play_game("Bob", (2, 7), (4, 5))

        self.assertEqual(game.game_winner(), "Game has not ended")


if __name__ == "__main__":
    unittest.main()