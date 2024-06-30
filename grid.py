from typing import Iterable, Union
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

from pieces import Piece, NUM_PIECES, movement_dict


# Grid size (including hidden cells)
N = 11

# Hexagon's apotheme (used for plotting)
APOTHEME = np.sin(np.radians(60))

# Special values for grid cells
FREE = 0
BLOCKED = -1
HIDDEN = -2
ERROR = -3
VISITED = -4

# Colors for special grid cells
color_map = {
	HIDDEN: "grey",
	BLOCKED: "black",
	FREE: "white",
	ERROR: "red",
}


# Pre-computed list of allowed values for the x coordinate and list of allowed 
# values for the y coordinate, given an x coordinate
allowed_xs_list = list(range(1, 10))
allowed_ys_lists = [
	list(range(max(6 - x, 1), 10 - max(0, x - 5)))
	for x in allowed_xs_list
]



class Grid:
    """
    Class for the game grid.

    The grid is an hexagonal grid, made of hexagonal cells (the real board is 
    different, but can be reduced to that), with a side of 6 cells.

    The board is represented as a normal matrix, but the coordinate system is 
    not perpendicular. In particular, the Y axis is rotated by 60 degrees 
    clockwise. Then, each cell can be represented with (x,y) coordinates, 
    where y is the row (parallel to the x axis) and x is the column (parallel 
    to the y axis).

    Each cell, has 6 neighbors (except for the one on the perimeter). The 
    perimeter of the grid is blocked, making the actual playable grid having 5 
    cells per side. 
    """

    def __init__(
        self,
        cmap_name: str = "inferno",
        pieces: Union[Piece, Iterable[Piece]] = None,
    ):
        self.grid = self.__init_grid()
        self.neighbors = self.__init_neighbors_lists()
        self.cmap = plt.get_cmap(cmap_name)
        if pieces is not None:
            self.add_pieces(pieces)


    @staticmethod
    def __init_grid():
        """
        Initializes the grid. No piece or contrain is added. Only the base,
        unchanging structure.
        """
        grid = np.full((N, N), FREE, dtype=int)
        # Fill Bottom row
        grid[0, :] = HIDDEN
        grid[0, -6:] = BLOCKED
        
        # Fill bottom half
        for r, c in enumerate(range(4, -1, -1)):
            grid[r+1, :c] = HIDDEN
            grid[r+1, c] = BLOCKED
            grid[r+1, -1] = BLOCKED

        # Fill top row
        grid[-1, :] = HIDDEN
        grid[-1, :6] = BLOCKED

        # Fill top half
        for r, c in enumerate(range(6, 1, -1)):
            rr = -(r+1)
            grid[rr, -c:] = HIDDEN
            grid[rr, -c] = BLOCKED
            grid[rr, 0] = BLOCKED
        
        return grid
    

    def __init_neighbors_lists(self):
        """
        Initializes the list of neighboring cells for each cell. Needed for 
        the feasibility check.
        """
        neighbors = np.empty((N, N), dtype=object)
        for x in allowed_xs_list:
            for y in allowed_ys_lists[x-1]:
                neighbors[y, x] = [
                    (x + mx, y + my)
                    for mx, my in movement_dict.values()
                    if self._is_point_valid(x + mx, y + my)
                ]
        return neighbors
    
    
    def _is_point_safe(self, x: int, y: int) -> bool:
        """
        Checks whether the given coordinates do not go outside the grid matrix 
        limits.
        """
        return (0 <= x < N) and (0 <= y < N)

    def _is_point_free(self, x: int, y: int) -> bool:
        """Checks whether the given coordinates are free."""
        return (
            self._is_point_safe(x, y) and
            self.grid[y, x] == FREE
        )

    def _is_point_valid(self, x: int, y: int) -> bool:
        """Checks whether the given coordinates are valid for the game."""
        return (
            self._is_point_safe(x, y) and
            self.grid[y, x] not in (HIDDEN, BLOCKED)
        )


    def is_impossible(self):
        """
        Checks whether the current grid configuration allows for solutions.

        This checks whether all the groups of connected free cells are 
        composed of a number of cells multiple of 5. This assumes all the 
        pieces are made of 5 components, and that the solution does not have 
        empty cells.
        """
        to_visit = []
        _grid = self.grid.copy()
        for x in allowed_xs_list:
            for y in allowed_ys_lists[x-1]:
                if _grid[y, x] != FREE:
                    continue

                # This is essentially a depth-first search
                to_visit.extend(self.neighbors[y, x])
                count = 1
                _grid[y, x] = VISITED
                while to_visit:
                    xn, yn = to_visit.pop()
                    if _grid[yn, xn] == FREE:
                        count += 1
                        _grid[yn, xn] = VISITED
                        to_visit.extend(self.neighbors[yn, xn])
                # Check group size
                if count % 5 != 0:
                    return True
        return False


    def add_piece(self, piece: Piece) -> bool:
        """
        Adds a piece to the grid.
        
        If at least one of the piece's components would end up in an invalid 
        or already occupied position, the piece is not inserted and `False` is 
        returned. Otherwise, the grid is updated and `True` is returned.
        """
        if not all(self._is_point_free(x, y) for x, y in piece):
            return False
        for x, y in piece:
            self.grid[y, x] = piece.index
        return True

    def add_pieces(self, pieces: Iterable[Piece]) -> bool:
        """
        Adds multiple pieces to the grid. The insertion stops as soon as one 
        of the pieces cannot be added.
        """
        for piece in pieces:
            if not self.add_piece(piece):
                return False
        return True

    def remove_piece(self, piece: Piece):
        """
        Removes a piece from the grid.

        Supposedly, the piece is exactly equal to one that was previously 
        added. No checks are performed on the validity or correctness of the 
        operation (for performance reasons).
        """
        # assert all(self._is_point_valid(x, y) for x, y in piece)
        for x, y in piece:
            self.grid[y, x] = FREE
    

    def draw(self, ax=None, show_hidden: bool = False):
        """Draws the grid."""
        if ax is None:
            ax = plt.gca()
        
        for row in range(N):
            y = 1.5 * row
            start_x = row * APOTHEME
            for col in range(N):
                x = start_x + 2 * APOTHEME * col
                val = self.grid[row, col]
                if val == HIDDEN and not show_hidden:
                    continue

                if val <= 0:
                    color = color_map[val]
                else:
                    color = self.cmap(val / NUM_PIECES)

                hex = RegularPolygon(
                    (x, y),
                    numVertices=6,
                    radius=1,
                    facecolor=color,
                    alpha=0.7,
                    edgecolor='black'
                )
                ax.add_patch(hex)

                if val > 0:
                    ax.text(
                        x, y,
                        str(self.grid[row, col]),
                        horizontalalignment="center",
                        verticalalignment="center",
                        fontsize=12,
                        color="black" if val >= 4 else "white",
                    )

