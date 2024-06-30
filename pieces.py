import sys


NUM_PIECES = 12


movement_dict = {
    0: (1, 0),    # Right
    1: (0, 1),    # Top right
    2: (-1, +1),  # Top left
    3: (-1, 0),   # Left
    4: (0, -1),   # Bottom left
    5: (+1, -1),  # Bottom right
}



class Piece:
    """
    Superclass for pieces. This defines the common behavior of all pieces.

    Subclasses should define a `movement` attribute containing the relative 
    position, in each of the three orientations, of the five piece's component 
    relative to a base component.

    Args:
        base_x (int): X (horizontal) coordinate of the base component
        base_y (int): Y (vertical) coordinate of the base component
        index (int): Piece type index
        rotation (int): Piece rotation. Either 0, 1 or 2
    """

    def __init__(
        self, base_x: int, base_y: int, index: int, rotation: int = 0
    ):
        self.base_x = base_x
        self.base_y = base_y
        self.index = index
        self.rotation = rotation % 3
        self.__make_coords()
    
    def __make_coords(self):
        """Pre-computes the concrete coordinates for the piece's components."""
        self.points = [
            (self.base_x + x, self.base_y + y)
            for x, y in self.movements[self.rotation]
        ]
    
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
        super().__init__(base_x, base_y, 1, rotation)


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
        super().__init__(base_x, base_y, 2, rotation)


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
        super().__init__(base_x, base_y, 3, rotation)


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
        super().__init__(base_x, base_y, 4, rotation)


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
        super().__init__(base_x, base_y, 5, rotation)


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
        super().__init__(base_x, base_y, 6, rotation)


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
        super().__init__(base_x, base_y, 7, rotation)


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
        super().__init__(base_x, base_y, 8, rotation)


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
        super().__init__(base_x, base_y, 9, rotation)


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
        super().__init__(base_x, base_y, 10, rotation)


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
        super().__init__(base_x, base_y, 11, rotation)


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
        super().__init__(base_x, base_y, 12, rotation)
