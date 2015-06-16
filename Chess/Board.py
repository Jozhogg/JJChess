"""Contains the Board class"""

import copy
import itertools
import Piece
import Move
from Piece import PieceType as p_type
from Piece import PieceColour as Colour
# Tkinter graphics package
from tkinter import *


class Board:

    """Contains a 2d array of pieces and methods for making/verifying moves.

    Attributes:
        - piece_array:  a 2d list of pieces

    """

    SIZE = 8
    FILE_LABELS = ["a", "b", "c", "d", "e", "f", "g", "h"]

    def __init__(self):
        """Create clear board."""
        self.clear()

        self.ver_hor_list = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        self.diag_list = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def draw_board(self, canvas):
        """Draw the current state of the board on a canvas.

        Args:
           - canvas : Tkinter canvas object to draw the board on

        """

        sq_width = int(canvas["width"])/8

        # white background
        canvas.create_rectangle(0, 0, sq_width*8, sq_width*8, fill="#FFCC66")

        # black squares: for each file draw 4 black squares
        for i in range(Board.SIZE):
            for j in range(int(Board.SIZE/2)):

                canvas.create_rectangle(i*sq_width, (2*j+(i+1) % 2)*sq_width,
                                        (i+1)*sq_width,
                                        (2*j+(i+1) % 2+1)*sq_width,
                                        fill="#401E00")

    def draw_pieces(self, canvas):

        sq_width = int(canvas["width"])/8

        # draw all pieces on the board
        for i in range(8):
            for j in range(8):

                self.piece_array[i][j].draw(canvas, i*sq_width, j*sq_width)

    def copy(self):
        return copy.deepcopy(self)

    def clear(self):
        """Initialise piece_array as an 8 x 8 array of blank pieces."""
        self.piece_array = [[Piece.Piece() for i in range(Board.SIZE)]
                            for i in range(Board.SIZE)]

    def setup(self):
        """Set the board to the arrangement for the beginning of a game."""

        self.clear()
        for x in range(Board.SIZE):
            self.piece_array[x][1] = Piece.Pawn(Colour.black)
            self.piece_array[x][6] = Piece.Pawn(Colour.white)

        self.piece_array[0][0] = Piece.Rook(Colour.black)
        self.piece_array[7][0] = Piece.Rook(Colour.black)
        self.piece_array[1][0] = Piece.Knight(Colour.black)
        self.piece_array[6][0] = Piece.Knight(Colour.black)
        self.piece_array[2][0] = Piece.Bishop(Colour.black)
        self.piece_array[5][0] = Piece.Bishop(Colour.black)
        self.piece_array[3][0] = Piece.Queen(Colour.black)
        self.piece_array[4][0] = Piece.King(Colour.black)

        self.piece_array[0][7] = Piece.Rook(Colour.white)
        self.piece_array[7][7] = Piece.Rook(Colour.white)
        self.piece_array[1][7] = Piece.Knight(Colour.white)
        self.piece_array[6][7] = Piece.Knight(Colour.white)
        self.piece_array[2][7] = Piece.Bishop(Colour.white)
        self.piece_array[5][7] = Piece.Bishop(Colour.white)
        self.piece_array[3][7] = Piece.Queen(Colour.white)
        self.piece_array[4][7] = Piece.King(Colour.white)

    def test_setup(self):

        for x in range(Board.SIZE):
            self.piece_array[x][1] = Piece.Pawn(Colour.black)
            self.piece_array[x][6] = Piece.Pawn(Colour.white)

        self.piece_array[0][0] = Piece.Rook(Colour.black)
        self.piece_array[7][3] = Piece.Rook(Colour.black)
        self.piece_array[1][4] = Piece.Knight(Colour.black)
        self.piece_array[6][7] = Piece.Knight(Colour.black)
        self.piece_array[2][1] = Piece.Bishop(Colour.black)
        self.piece_array[5][0] = Piece.Bishop(Colour.black)
        self.piece_array[3][2] = Piece.Queen(Colour.black)
        self.piece_array[4][0] = Piece.King(Colour.black)

        self.piece_array[0][4] = Piece.Rook(Colour.white)
        self.piece_array[7][7] = Piece.Rook(Colour.white)
        self.piece_array[1][7] = Piece.Knight(Colour.white)
        self.piece_array[6][5] = Piece.Knight(Colour.white)
        self.piece_array[2][7] = Piece.Bishop(Colour.white)
        self.piece_array[5][5] = Piece.Bishop(Colour.white)
        self.piece_array[3][6] = Piece.Queen(Colour.white)
        self.piece_array[4][2] = Piece.King(Colour.white)


    def make_move(self, move):
        """Adjust the state of the board to reflect the passed move.

        The universe may explode if this is not a legal move.

        Args:
            - move:  a Move object
        """
        if move.castle:
            self.castle(move)
            return

        if move.en_passant:
            self.remove_piece(*move.en_passant_posn)

        piece = self.piece_array[move.start_posn[0]][move.start_posn[1]]

        self.remove_piece(*move.start_posn)
        self.place_piece(move.end_posn[0], move.end_posn[1],
                         piece.type, piece.colour)

    def takeback_move(self, move, taken_piece):

        if move.castle:
            self.takeback_castle(move)
            return

        piece = self.piece_array[move.end_posn[0]][move.end_posn[1]]

        if move.en_passant:
            if piece.colour == Colour.white:
                self.place_piece(move.en_passant_posn[0], 
                                 move.en_passant_posn[1],
                                 p_type.pawn, Colour.black)
            else:
                self.place_piece(move.en_passant_posn[0], 
                                 move.en_passant_posn[1],
                                 p_type.pawn, Colour.white)

        

        self.remove_piece(*move.end_posn)
        self.place_piece(move.start_posn[0], move.start_posn[1],
                         piece.type, piece.colour)

        if taken_piece is not None:

            self.place_piece(move.end_posn[0], move.end_posn[1],
                             taken_piece.type, taken_piece.colour)

    def castle(self, move):
        """Adjust the state of the board to reflect the passed castling move.

        The passed move should be a legal castling move.

        Args:
            - move: a move object which is a castling move.
        """

        piece = self.piece_array[move.start_posn[0]][move.start_posn[1]]
        col = piece.colour

        # If king is moving to the right
        if move.end_posn[0] - move.start_posn[0] > 0:
            # Castling King's side
            rook_from_x = 7
            rook_to_x = 5
        else:
            # Castling Queen's side
            rook_from_x = 0
            rook_to_x = 3

        rook_y = move.start_posn[1]

        # Move the king
        self.make_move(Move.Move(move.start_posn, move.end_posn))

        # Move the rook
        self.remove_piece(rook_from_x, rook_y)
        self.place_piece(rook_to_x, rook_y, p_type.rook, col)

    def takeback_castle(self, move):

        piece = self.piece_array[move.start_posn[0]][move.start_posn[1]]
        col = piece.colour

        # If king is moving to the right
        if move.end_posn[0] - move.start_posn[0] > 0:
            # Castling King's side
            rook_from_x = 7
            rook_to_x = 5
        else:
            # Castling Queen's side
            rook_from_x = 0
            rook_to_x = 3

        rook_y = move.start_posn[1]

        # Move the king
        self.takeback_move(Move.Move(move.start_posn, move.end_posn), None)

        # Move the rook
        self.remove_piece(rook_to_x, rook_y)
        self.place_piece(rook_from_x, rook_y, p_type.rook, col)

    def promote_pawn(self, piece_colour, piece_type):
        """Promote a pawn of a given colour to the given piece type.

        Args:
            - piece_colour:  a member of the PieceColour enum
            - piece_type:  a member of the PieceType enum

        Raises:
            - TypeError if there is no valid pawn to promote.

        """

        if (piece_colour == Colour.white):
            y = 0
        else:
            y = 7

        for i in range(Board.SIZE):
            if self.piece_array[i][y] == Piece.Pawn(piece_colour):
                self.place_piece(i, y, piece_type, piece_colour)
                break
        else:
            raise TypeError(
                "Promote Pawn called, but no pawn is available for promotion.")

    ###########################################################################
    ############################# HELPER FUNCTIONS ############################
    ###########################################################################

    def is_square(self, x, y):
        """Return true if (x, y) represents a valid square."""
        return (x < 8 and y < 8 and x >= 0 and y >= 0)

    def get_piece(self, x, y):
        """Return the piece at position x, y on the board.

        Returns None if indeices out of bounds
        """
        
        try:
            piece = self.piece_array[x][y]
        except IndexError:
            return None

        if(not self.is_square(x, y)):
            return None

        return piece

    def place_piece(self, x, y, piece_type, piece_colour):
        """Place a piece of the passed type at the passed location.

        Args:
            - x, y:  ints specifying the position on the board to place piece
            - type:  a member of the PieceType enum
            - piece_colour:  a member of the PieceColour enum

        Will raise IndexError if the indices are not valid.
        """

        self.piece_array[x][y] = Piece.make_piece(piece_type, piece_colour)

    def remove_piece(self, x, y):
        """Remove the piece at the passed location.

        Args:
            - x, y:  ints specifying the position on the board to remove piece

        Will raise IndexError if the indices are not valid.
        """

        self.piece_array[x][y] = Piece.Piece()

    def search_direction(self, x, y, up_down, left_right, no_legal=False):
        """Move along the board in a given direction and return information.

        Given a starting location and a direction, move along the board in
        that direction and return a tuple with information about the number of
        empty squares, the piece at the end of the search, and what moves are
        legal.

        Args:
            - x, y:  ints specifying the position on the board to start at
            - up_down:  int, positive if moving upwards (in the negative y
                        direction), negative if moving downwards
            - left_right:  int, positive if moving right (in the positive
                           x direction), negative if moving left
            - no_legal:  If this is set true, the function will skip
                         calculating a list of valid possible moves (which can
                         be slow)

        For instance, up_down = 1 and left_right = -1 would look diagonally
        up and to the left.

        Returns: a tuple containing three pieces of information:
            [0] An integer count of the number of empty squares before the
                function finds another piece. This will be zero if there is
                a piece right next to (x, y). If the function reaches the end
                of the board, this will be the number of empty squares
                between (x, y) and the edge of the board (zero if (x, y) is at
                the edge of the board).
            [1] The piece the function finds at the end of the search, or None
                if the function reaches the edge of the board without finding a
                piece
            [2] A list of moves which are valid and possible for a piece at
                (x, y) in the given direction (or empty list if no_legal is 
                true)

        Will raise ValueError if up_down == left_right == 0, or IndexError if
        x and y do not refer to a physical square on the board.

        """

        #John, Not sure what these functions are doing. Commented them out
        #for now as quite slow especially as this function is called a lot.

        #if(up_down != 0):
        #    up_down = int(up_down/abs(up_down))

        #if(left_right != 0):
        #    left_right = int(left_right/abs(left_right))

        #if up_down == 0 and left_right == 0:
        #    raise ValueError

        #if not self.is_square(x, y):
        #    raise IndexError

        num_squares = 0
        found_piece = None
        move_list = []

        new_x = x
        new_y = y

        new_x += left_right
        new_y += up_down

        while(self.is_square(new_x, new_y)):

            piece_at_move = self.piece_array[new_x][new_y]

            if not no_legal:
                move = Move.Move((x, y), (new_x, new_y))

                if self.is_possible_valid_move(move):
                    move_list.append(move)

            if piece_at_move.type != p_type.blank:
                found_piece = piece_at_move
                break

            num_squares += 1
            new_x += left_right
            new_y += up_down

        return (num_squares, found_piece, move_list)

    ###########################################################################
    ############################# MOVE EVALUATION #############################
    ###########################################################################

    def is_possible_move(self, move):
        """Return True if the passed move is possible.

        A move is POSSIBLE if it takes a piece to a square that:
          - exists on the board, and
          - does not contain another piece of the same colour.

        A castling move is considered POSSIBLE if the king and rook are in the
        correct position and the space between them is empty.

        Args:
            - move:  a Move object

        """

        if move.castle:
            return self.is_possible_castle_move(move)

        piece_moving = self.piece_array[move.start_posn[0]][move.start_posn[1]]

        piece_at_move = self.get_piece(*move.end_posn)

        if piece_at_move is None:
            return False

        if (piece_at_move.colour == piece_moving.colour):
            return False

        return True

    def is_valid_move(self, move):
        """Return true if the passed move is valid.

        A move is valid if after is it made, the king of the player who made it
        is not in check.

        Args:
            - move:  a Move object

        """

        if move.castle:
            return self.is_valid_castle_move(move)

        piece_moving = self.piece_array[move.start_posn[0]][move.start_posn[1]]
        taken_piece = self.get_piece(*move.end_posn)

        #SLOW
        #new_board = self.copy()
        #new_board.make_move(move)

        #if new_board.is_in_check(piece_moving.colour):
        #    return False

        #FAST
        self.make_move(move)

        if self.is_in_check(piece_moving.colour):

            self.takeback_move(move, taken_piece)

            return False

        self.takeback_move(move, taken_piece)

        return True

    def is_possible_castle_move(self, move):
        """Return true if the passed move is a castle move and is possible.

        A castling move is considered POSSIBLE if the king and rook are in the
        correct position and the space between them is empty.

        Args:
            - move:  a Move object

        """

        if not move.castle:
            return False

        king = self.piece_array[move.start_posn[0]][move.start_posn[1]]

        if king.type != p_type.king:
            return False

        if king.colour == Colour.white:
            y = 7
            friendly_rook = Piece.Rook(Colour.white)
        elif king.colour == Colour.black:
            y = 0
            friendly_rook = Piece.Rook(Colour.black)

        # If king is not at correct position for castling
        if move.start_posn != (4, y):
            return False

        if (move.end_posn[0] > move.start_posn[0]):
            # Castling King's side

            search_results = self.search_direction(
                move.start_posn[0], move.start_posn[1], 0, 1, no_legal=True)
            if search_results[0] != 2:
                return False
            if search_results[1] != friendly_rook:
                return False
        else:
            # Castling Queen's side
            search_results = self.search_direction(
                move.start_posn[0], move.start_posn[1], 0, -1, no_legal=True)
            if search_results[0] != 3:
                return False
            if search_results[1] != friendly_rook:
                return False

        return True

    def is_valid_castle_move(self, move):
        """Return true if the passed move is a castle move and is valid.

        A castling move is VALID if by making it, the king does not castle
        into, out of, or through check. Note that this function will return
        true if a castling move is valid, regardless of whether the king/rook
        has already moved.

        Args:
            - move:  a Move object

        """

        if not move.castle:
            return False

        king = self.piece_array[move.start_posn[0]][move.start_posn[1]]

        if self.is_in_check(king.colour):
            return False

        if (move.end_posn[0] > move.start_posn[0]):
            # Castling King's side

            search_results = self.search_direction(
                move.start_posn[0], move.start_posn[1], 0, 1)
            if len(search_results[2]) != 2:
                return False
        else:
            # Castling Queen's side

            search_results = self.search_direction(
                move.start_posn[0], move.start_posn[1], 0, -1)
            if len(search_results[2]) != 3:
                return False

        return True

    def is_possible_valid_move(self, move):
        """Return true if the passed move is both possible and valid."""
        return (self.is_possible_move(move) and self.is_valid_move(move))

    def is_take_move(self, move):
        """Return true if the passed move is a taking move."""
        piece_at_move = self.piece_array[move.end_posn[0]][move.end_posn[1]]

        return piece_at_move.type != p_type.blank

    ###########################################################################
    ############################## MOVE FETCHING ##############################
    ###########################################################################

    def get_piece_moves(self, x, y):
        """Return a list of available moves for the piece at (x, y).

        Given a position (x, y), return a list of moves which it is legal for
        the piece at (x, y) to make. Note that this list is not completely
        exhaustive: the function will not return any castle moves or en passant
        moves.

        """

        piece_to_move = self.piece_array[x][y]

        if piece_to_move.type == p_type.king:
            return self.get_king_moves(x, y)
        if piece_to_move.type == p_type.queen:
            return self.get_queen_moves(x, y)
        if piece_to_move.type == p_type.bishop:
            return self.get_bishop_moves(x, y)
        if piece_to_move.type == p_type.knight:
            return self.get_knight_moves(x, y)
        if piece_to_move.type == p_type.rook:
            return self.get_rook_moves(x, y)
        if piece_to_move.type == p_type.pawn:
            return self.get_pawn_moves(x, y)

        return []

    def get_king_moves(self, x, y):
        """Return a list of available moves for a king at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a king at (x, y) to make, excluding castling moves. If the piece at
        (x, y) is not a king or there is more than one king of a given colour
        on the board, this function will return without error but with
        incorrect results.

        """

        move_list = []
        square_list = [(x+1, y+1), (x+1, y),   (x+1, y-1), (x, y+1),
                       (x, y-1),   (x-1, y+1), (x-1, y),   (x-1, y-1)]

        for square in square_list:
            move = Move.Move((x, y), square)
            if self.is_possible_valid_move(move):
                move_list.append(move)

        return move_list

    def get_queen_moves(self, x, y):
        """Return a list of available moves for a queen at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a queen at (x, y) to make.

        """

        move_list = []
        move_list.extend(self.get_bishop_moves(x, y))
        move_list.extend(self.get_rook_moves(x, y))
        return move_list

    def get_bishop_moves(self, x, y):
        """Return a list of available moves for a bishop at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a bishop at (x, y) to make.

        """

        move_list = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for direction in directions:
            direction_moves = self.search_direction(
                x, y, direction[0], direction[1])
            move_list.extend(direction_moves[2])

        return move_list

    def get_knight_moves(self, x, y):
        """Return a list of available moves for a knight at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a knight at (x, y) to make.

        """

        move_list = []
        square_list = [(x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
                       (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)]

        for square in square_list:
            move = Move.Move((x, y), square)
            if self.is_possible_valid_move(move):
                move_list.append(move)

        return move_list

    def get_rook_moves(self, x, y):
        """Return a list of available moves for a rook at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a rook at (x, y) to make.

        """

        move_list = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for direction in directions:
            direction_moves = self.search_direction(
                x, y, direction[0], direction[1])
            move_list.extend(direction_moves[2])

        return move_list

    def get_pawn_moves(self, x, y):
        """Return a list of available moves for a pawn at (x, y).

        Given a position (x, y) returns a list of moves which it is legal for
        a pawn at (x, y) to make, excluding en passant moves.

        """

        move_list = []
        can_double = False   # True if the pawn can move two squares forward.
        pawn = self.piece_array[x][y]

        if pawn.colour == Colour.white:
            m = -1  # m is a multiplier which ensures white pieces move up the
            # board (in the negative y direction) and vice versa

            if y == 6:
                can_double = True
        elif pawn.colour == Colour.black:
            m = 1

            if y == 1:
                can_double = True

        one_forward = Move.Move((x, y), (x, y + 1*m))
        two_forward = Move.Move((x, y), (x, y + 2*m))
        left_take = Move.Move((x, y), (x - 1, y + 1*m))
        right_take = Move.Move((x, y), (x + 1, y + 1*m))

        if (self.is_possible_valid_move(one_forward)
                and not self.is_take_move(one_forward)):
            move_list.append(one_forward)

            if (self.is_possible_valid_move(two_forward)
                    and can_double
                    and not self.is_take_move(two_forward)):
                move_list.append(two_forward)

        if (self.is_possible_valid_move(left_take)):
            if (self.is_take_move(left_take)):
                move_list.append(left_take)

        if (self.is_possible_valid_move(right_take)):
            if (self.is_take_move(right_take)):
                move_list.append(right_take)

        return move_list

    ###########################################################################
    ############################ BOARD EVALUATION #############################
    ###########################################################################

    def is_in_check(self, piece_colour):
        """Return true if the king of the passed colour is in check.

        Note that if no king of the passed colour is found, this function will
        return false.

        Args:
            piece_colour:  a member of the Piece.PieceColour enum

        """

        # Find King
        for i, j in itertools.product(range(Board.SIZE), range(Board.SIZE)):
            piece = self.piece_array[i][j]
            if piece.type == p_type.king and piece.colour == piece_colour:
                x = i
                y = j
                break
        else:
            return False

        # Radiate outwards and check for enemy rooks, bishops and queens:

        # Look for pawns
        
        square_list = [(x+1, y-piece_colour), (x-1, y-piece_colour)]

        for square in square_list:
            piece = self.get_piece(*square)
            if piece is not None:
                if piece.type == p_type.pawn:
                    if piece.colour != piece_colour:
                        return True

        # Look for knights
        square_list = [(x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
                       (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)]

        for square in square_list:
            piece = self.get_piece(*square)
            if piece is not None:
                if piece.type == p_type.knight:
                    if piece.colour != piece_colour:
                        return True

        # The enemy king
        square_list = [(x+1, y+1), (x+1, y),   (x+1, y-1), (x, y+1),
                       (x, y-1),   (x-1, y+1), (x-1, y),   (x-1, y-1)]

        for square in square_list:
            piece = self.get_piece(*square)
            if piece is not None:
                if piece.type == p_type.king:
                    if piece.colour != piece_colour:
                        return True

        # Vertically/Horizontally
        for dirn in self.ver_hor_list:
            piece = self.search_direction(
                x, y, dirn[0], dirn[1], no_legal=True)[1]

            if piece is not None:
                if piece.type in (p_type.rook, p_type.queen):
                    if piece.colour != piece_colour:
                        return True

        # And Finally, Diagonally
        for dirn in self.diag_list:
            piece = self.search_direction(
                x, y, dirn[0], dirn[1], no_legal=True)[1]

            if piece is not None:
                if piece.type in (p_type.bishop, p_type.queen):
                    if piece.colour != piece_colour:
                        return True

        return False

    def has_won(self, piece_colour):
        """Return true if the team of the passed colour has won.

        Args:
            - piece_colour:  a member of the Piece.PieceColour enum

        """

        if piece_colour == colour.white:
            enemy = Colour.black
        else:
            enemy = Colour.white

        return (not legal_move_exists(enemy)) and self.is_in_check(enemy)

    def legal_move_exists(self, piece_colour):
        """Return true if the team of the passed colour can make a legal move.

        Args:
            - piece_colour:  a member of the Piece.PieceColour enum

        """

        for i, j in itertools.product(range(Board.SIZE), range(Board.SIZE)):
            piece = self.get_piece(i, j)
            if piece.colour == piece_colour:
                if len(self.get_piece_moves(i, j)) > 0:
                    return True

        return False

    def is_king_draw(self):
        """Return true if the Kings are the only pieces left on the board."""
        for i, j in itertools.product(range(Board.SIZE), range(Board.SIZE)):
            piece = self.piece_array[i][j]
            if not piece.type in (p_type.king, p_type.blank):
                return False

        return True

    def can_promote_pawn(self, piece_colour):
        """Return true if the player of passed colour can promote a pawn."""

        if (piece_colour == Colour.white):
            y = 0
        else:
            y = 7

        for i in range(Board.SIZE):
            # if self.get_piece(i, y) == Piece.Pawn(piece_colour):
            if self.piece_array[i][y].type == p_type.pawn:
                return True

        return False

    ###########################################################################
    ########################### BOARD REPRESENTATION ##########################
    ###########################################################################

    def get_san(self, move):
        """Return a SAN representation of move (ignoring checks/promotions).

           Args:
               -move: the move to return SAN of
        """
        san = ""

        if(move.castle):

            san += "O-O"

            # Check if queenside
            if(move.end_posn == (0, 0) or move.end_posn == (0, 7)):

                san += "-O"

        else:
            piece = self.piece_array[move.start_posn[0]][move.start_posn[1]]

            if(piece.type != p_type.pawn):
                san += piece.get_san().upper()
                san += self.get_clar_str(move, piece)

            if self.is_take_move(move):

                if piece.type == p_type.pawn:
                    # If pawn we only give the file (no clarification needed)
                    san += Board.FILE_LABELS[move.start_posn[0]]

                san += "x"

            san += Board.FILE_LABELS[move.end_posn[0]] + \
                str(8-move.end_posn[1])

        return san

    def get_clar_str(self, move, piece):
        """Create a clarification string for SAN if required.

           Used to dissambiguate piece moves where more than one piece of a 
           a given type can reach the target square

           Args:
               - move: the move that has been made
               - piece: the piece being moved
        """

        clar_str = ""
        need_file = False
        need_rank = False

        for i in range(Board.SIZE):
            for j in range(Board.SIZE):

                if not (i == move.start_posn[0] and j == move.start_posn[1]):

                    if self.piece_array[i][j].colour == piece.colour:

                        if(self.piece_array[i][j].type == piece.type):

                            moves_list = self.get_piece_moves(i, j)

                            for m in moves_list:

                                if(m.end_posn == move.end_posn):

                                    if(i == move.start_posn[0]):
                                        need_rank = True

                                    else:
                                        need_file = True

        if(need_file):
            clar_str += Board.FILE_LABELS[move.start_posn[0]]
        if(need_rank):
            clar_str += str(8-move.start_posn[1])

        return clar_str

    def get_pictorial(self):
        """Return a pictorial string representation of the board."""
        board_str = "\n"
        board_str += "------------------\n"

        for i in range(Board.SIZE):
            board_str += "|"

            for j in range(Board.SIZE):
                board_str += self.piece_array[j][i].get_san() + " "

            board_str += "|\n"

        board_str += "------------------\n\n"

        return board_str

    def get_forsyth(self):
        """Return a string representation of the board in FEN.

        The string will have one space at the end.

        """

        forsyth = ""

        for row in range(Board.SIZE):
            column = 0

            while column < BOARD_SIZE:
                piece = self.piece_array[column][row]

                if piece.type == p_type.blank:
                    gap = self.search_direction(
                        column, row, 0, 1, no_legal=True)[0]
                    forsyth += str(gap + 1)
                    column += gap + 1
                else:
                    forsyth += piece.get_san()
                    gap = searchDirection(
                        column, row, 0, 1, no_legal=True)[0]

                    if gap > 0:
                        forsyth += str(gap)
                    column += gap + 1

            if row < BOARD_SIZE - 1:
                forsyth += "/"

        forsyth += " "
        return forsyth
