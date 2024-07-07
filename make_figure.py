import argparse

import matplotlib.pyplot as plt
import yaml

from grid import BLOCKED, Grid
from pieces import get_piece



def load_solution(filename: str) -> Grid:
    """
    Loads solution to a problem from a YAML configuration file.

    The config file should contain the following entries:

    - 'blocked_grid_cells': This should be a list of (x, y) couples 
      corresponding to the x and y coordinates of the blocked grid cells.

    - 'solution': ...

    Args:
        filename (str): Configuration file name (yaml).
    
    Returns:
        Grid: Solved grid (with all the pieces placed).
    """
    with open(filename, "r") as fp:
        problem_conf = yaml.safe_load(fp)
    
    grid = Grid()
    for x, y in problem_conf["blocked_grid_cells"]:
        grid.grid[y, x] = BLOCKED
        
    for index, piece_conf in problem_conf["solution"].items():
        piece = get_piece(index, **piece_conf)
        if not grid.add_piece(piece):
            raise RuntimeError(f"Invalid solution! Cannot add piece {piece}")

    return grid



def make_figure(
    config_file: str,
    figure_file: str,
):
    """
    Generates and save a figure showing the solution to a problem.

    The problem is loaded from a configuration file containing the initial 
    grid configuration and the set of pieces solving the problem.

    Args:
        config_file (str): Problem configuration file (yaml).
        figure_file (str): Generated image file.
    """

    grid = load_solution(config_file)

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    grid.draw(ax=ax)
    ax.set(xlim=(2, 23), ylim=(-3, 18))
    ax.set_aspect("equal")
    plt.axis("off")
    fig.tight_layout()
    fig.savefig(figure_file)

    plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Makes a solution image.")
    parser.add_argument(
        "config_file", help="Problem configuration file (YAML)"
    )
    parser.add_argument(
        "filename", help="Name of the file to generate"
    )

    args = parser.parse_args()

    make_figure(
        config_file=args.config_file,
        figure_file=args.filename,
    )
