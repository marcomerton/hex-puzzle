"""
This module contains a general `Piece` class, implementing the common interface 
of all pieces and the definition of the 12 concrete pieces in the game 
(excluded the single cell piece used to contrain the solution).

For all the pieces, the position of their five components relative to the base 
coordinate, for the 3 possible rotations, are pre-computed and stored as class 
attributes.
"""

import sys


NUM_PIECES = 12


# Relative position (x, y) of the 6 neighbors of a cell
movement_dict = {
    0: (1, 0),    # Right
    1: (0, 1),    # Top right
    2: (-1, +1),  # Top left
    3: (-1, 0),   # Left
    4: (0, -1),   # Bottom left
    5: (+1, -1),  # Bottom right
}


# Pre-computed list of possible piece rotations
rot_list = list(range(3))



class Piece:
    """
    Superclass for pieces. This defines the common behavior of all pieces.

    Subclasses should define a `movement` attribute containing the position, 
    in each of the three possible rotations, of the five piece's component 
    relative to a base component.

    Args:
        base_x (int): X (horizontal) coordinate of the base component
        base_y (int): Y (vertical) coordinate of the base component
        index (int): Piece type index
        rotation (int): Piece rotation. Either 0, 1 or 2
    """

    def __init__(
        self, index: int, base_x: int = 0, base_y: int = 0, rotation: int = 0
    ):
        self.index = index
        self.base_x = base_x
        self.base_y = base_y
        self.rotation = rotation % 3
        self.__make_coords()
    
    def __make_coords(self):
        """Pre-computes the concrete coordinates for the piece's components."""
        self.points = [
            (self.base_x + x, self.base_y + y)
            for x, y in self.movements[self.rotation]
        ]
    
    def __str__(self) -> str:
        """To-string magic method."""
        return (
            f"Piece{self.index}("
            f"x={self.base_x}, "
            f"y={self.base_y}, "
            f"rot={self.rotation})"
        )

    def __iter__(self):
        """Iterator over piece's components."""
        return iter(self.points)

    def make_new(self, x: int, y: int, rot: int) -> "Piece":
        """
        Makes a new Piece, of the same type, with the given base coordinates 
        and rotation.

        Args:
            x (int): New base's x coordinate
            y (int): New base's y coordinate
            rot (int): New rotation
        
        Return:
            Piece: New piece in the given position/rotation
        """
        return type(self)(x, y, rot)


def get_piece(idx: int, *args, **kwargs) -> Piece:
    """Makes a new Piece of type `idx`."""
    _name = "Piece" + str(idx)
    _class = getattr(sys.modules[__name__], _name)
    return _class(*args, **kwargs)



class Piece1(Piece):
    """
    Shape of the piece with rotation 0:
         O
    O O O
         O
    """
    movements = [
        [(0, 0), (1, 0), (2, 0), (2, 1), (3, -1)],
        [(0, 0), (-1, 1), (-2, 2), (-3, 2), (-2, 3)],
        [(0, 0), (0, -1), (0, -2), (1, -3), (-1, -2)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(1, base_x, base_y, rotation)


class Piece2(Piece):
    """
    Shape of the piece with rotation 0:
    O O
     O
      O
     O
    """
    movements = [
        [(0, 0), (0, 1), (-1, 2), (-1, 3), (-2, 3)],
        [(0, 0), (-1, 0), (-1, -1), (-2, -1), (-1, -2)],
        [(0, 0), (1, -1), (2, -1), (3, -2), (3, -1)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(2, base_x, base_y, rotation)


class Piece3(Piece):
    """
    Shape of the piece with rotation 0:
         O O
    O O O
    """
    movements = [
        [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],
        [(0, 0), (-1, 1), (-2, 2), (-3, 2), (-4, 3)],
        [(0, 0), (0, -1), (0, -2), (1, -3), (1, -4)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(3, base_x, base_y, rotation)


class Piece4(Piece):
    """
    Shape of the piece with rotation 0:
    O   O
     O O O
    """
    movements = [
        [(0, 0), (1, -1), (2, -1), (3, -1), (2, 0)],
        [(0, 0), (0, 1), (-1, 2), (-2, 3), (-2, 2)],
        [(0, 0), (-1, 0), (-1, -1), (-1, -2), (0, -2)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(4, base_x, base_y, rotation)


class Piece5(Piece):
    """
    Shape of the piece with rotation 0:
    O O O O
         O
    """
    movements = [
        [(0, 0), (1, 0), (2, 0), (3, 0), (3, -1)],
        [(0, 0), (-1, 1), (-2, 2), (-3, 3), (-2, 3)],
        [(0, 0), (0, -1), (0, -2), (0, -3), (-1, -2)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(5, base_x, base_y, rotation)


class Piece6(Piece):
    """
    Shape of the piece with rotation 0:
    O
     O
      O O O
    """
    movements = [
        [(0, 0), (-1, 0), (-2, 0), (-3, 1), (-4, 2)],
        [(0, 0), (1, -1), (2, -2), (2, -3), (2, -4)],
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(6, base_x, base_y, rotation)


class Piece7(Piece):
    """
    Shape of the piece with rotation 0:
     O
      O
     O O O
    """
    movements = [
        [(0, 0), (-1, 0), (-2, 0), (-2, 1), (-3, 2)],
        [(0, 0), (1, -1), (2, -2), (1, -2), (1, -3)],
        [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(7, base_x, base_y, rotation)


class Piece8(Piece):
    """
    Shape of the piece with rotation 0:
     O O O O
    O
    """
    movements = [
        [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1)],
        [(0, 0), (-1, 0), (-2, 1), (-3, 2), (-4, 3)],
        [(0, 0), (1, -1), (1, -2), (1, -3), (1, -4)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(8, base_x, base_y, rotation)


class Piece9(Piece):
    """
    Shape of the piece with rotation 0:
      O
     O
    O O
     O
    """
    movements = [
        [(0, 0), (0, 1), (-1, 1), (-1, 2), (-1, 3)],
        [(0, 0), (-1, 0), (0, -1), (-1, -1), (-2, -1)],
        [(0, 0), (1, -1), (1, 0), (2, -1), (3, -2)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(9, base_x, base_y, rotation)


class Piece10(Piece):
    """
    Shape of the piece with rotation 0:
        O
       O O
    O O
    """
    movements = [
        [(0, 0), (1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 0), (-1, 1), (-2, 1), (-3, 2), (-3, 1)],
        [(0, 0), (0, -1), (1, -2), (1, -3), (2, -3)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(10, base_x, base_y, rotation)


class Piece11(Piece):
    """
    Shape of the piece with rotation 0:
         O
    O O O
       O
    """
    movements = [
        [(0, 0), (1, 0), (2, -1), (2, 0), (2, 1)],
        [(0, 0), (-1, 1), (-1, 2), (-2, 2), (-3, 2)],
        [(0, 0), (0, -1), (-1, -1), (0, -2), (1, -3)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(11, base_x, base_y, rotation)


class Piece12(Piece):
    """
    Shape of the piece with rotation 0:
     O O O
    O O
    """
    movements = [
        [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (-1, 1), (-1, 0), (-2, 1), (-3, 2)],
        [(0, 0), (0, -1), (1, -1), (1, -2), (1, -3)],
    ]
    def __init__(self, base_x: int = 0, base_y: int = 0, rotation: int = 0):
        super().__init__(12, base_x, base_y, rotation)
