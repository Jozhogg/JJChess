"""Contains the Move class"""


class Move:

    """Contains all information required to make or display a move.

    Attributes:
        - castle:  true if the move is a castling move
        - en_passant:  true if the move is an enPassant move
        - start_posn:  an integer tuple containing the x and y values of the
                      piece (king if castling move) making the move
        - end_posn:  an integer tuple containing the x and y values of the
                    square the piece (king if castling move) is moving to
        - en_passant_posn:  if en_passant, this is a tuple containing the x and
                            y values of the pawn which will be taken by the move

    """

    def __init__(self, start_posn, end_posn, castle=False, en_passant=False,
                 en_passant_posn=None):
        """Initialise a move according to passed parameters."""

        if castle and en_passant:
            raise ValueError("Castle and en_passant cannot both be true")

        if (en_passant and en_passant_posn is None):
            raise ValueError("Must provide en_passant_posn")

        self.start_posn = start_posn
        self.end_posn = end_posn
        self.castle = castle
        self.en_passant = en_passant
        self.en_passant_posn = en_passant_posn

    def __eq__(self, other):
        return (self.start_posn == other.start_posn
                and self.end_posn == other.colour
                 and self.castle == other.castle
                  and self.en_passant == other.en_passant
                   and self.en_passant_posn == other.en_passant_posn)
        
    def __ne__(self, other):
        return not self.__eq__(other)
