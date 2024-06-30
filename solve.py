import random
import time
from typing import List, Optional, Tuple

import yaml

import matplotlib.pyplot as plt


from grid import (
    allowed_xs_list,
    allowed_ys_lists,
	BLOCKED,
    Grid,
)

from pieces import get_piece, NUM_PIECES, Piece




rot_list = list(range(3))


def solve_recursive(
	grid: Grid,
	pieces: List[Piece],
	index: int = 0,
	check_at: int = 5
) -> bool:
	"""
	Recursive function to solve a problem.

	The idea is that, once a piece is positioned, the problem becomes an 
	easier problem, with one piece left and a different starting grid.

	This function, given a grid state (with possibly some piece already 
	positioned) and a piece (as an index in a list of pieces), tries to find a
	valid position for the piece. Once this is found, it recusively call itself.

	Args:
		grid (Grid): Problem grid.
		pieces (list): List of pieces for the problem.
		index (int): Index (in the list) of the current piece.
		check_at (int): Index from which checking if the grid is solvable 
			See grid.is_impossible() for details.
	"""
	if index == len(pieces):
		return True
	
	if index >= check_at and grid.is_impossible():
		return False

	piece = pieces[index]
	for rot in rot_list:
		for x in allowed_xs_list:
			for y in allowed_ys_lists[x-1]:
				piece = piece.make_new(x, y, rot)
				is_placed = grid.add_piece(piece)

				if is_placed:
					if solve_recursive(grid, pieces, index+1, check_at):
							pieces[index] = piece
							return True

					grid.remove_piece(piece)

	return False



# === Iterative solver ===
# Initial tests didn't show much advantage in avoiding recursion.
# Hence, this might not work now.

def config_gen(piece):
	for rot in rot_list:
		for x in allowed_xs_list:
			for y in allowed_ys_lists[x-1]:
				yield piece.make_new(x, y, rot)

def search_piece_position(grid, generator):
	for piece in generator:
		if grid.add_piece(piece):
			return piece, generator
	return None


def solve_iter(grid, pieces, check_at=5) -> bool:
	generators = [config_gen(piece) for piece in pieces]
	idx = 0

	while idx < len(pieces):
		piece, gen = pieces[idx], generators[idx]
		res = search_piece_position(grid, gen)

		if res is not None:
			# If a position is found
			if idx >= check_at and grid.check_isolated():
				grid.remove_piece(res[0])
				continue

			pieces[idx] = res[0]
			generators[idx] = res[1]
			idx += 1

		else:
			# If no position is found
			if idx == 0:
				return False

			generators[idx] = config_gen(piece)
			idx -= 1
			grid.remove_piece(pieces[idx])

	return True

# === Iterative solver ===



def prepare_problem(filename: str) -> Tuple[Grid, List[Piece]]:
	"""
	Loads a problem from a configuration file.

	Args:
		filename (str): Configuration file name (yaml)
	
	Returns:
		Grid, List: Starting grid and list of available pieces
	"""
	with open(filename, "r") as fp:
		problem_conf = yaml.safe_load(fp)
	
	grid = Grid()
	for x, y in problem_conf["blocked_grid_points"]:
		grid.grid[y, x] = BLOCKED
	assert not grid.is_impossible()

	pieces = [
		get_piece(i)
		for i in range(1, NUM_PIECES+1)
		if i not in problem_conf["excluded_pieces"]
	]

	return grid, pieces



def solve(
	filename: str,
	seed: Optional[int] = None,
	use_iterative: bool = False,
	check_at: int = 5,
	save_figure: bool = False,
	figure_filename: Optional[str] = None,
	save_solution: bool = False,
):
	"""
	...

	Args:
		filename (str): Problem configuration file (yaml)
		seed (int, optional): Seed for the random number generator. This 
			influences the order of the pieces
		use_iterative (bool): Ignored...
		check_at (int): Number of pieces placed after which starting to check 
			if the grid is solvable
		save_figure (bool): Whether to save the solution as a figure
		figure_filename (str, optional): File where the figure is saved
		save_solution (bool): Whether to save the solution in the input config 
			file
	"""
	assert not save_figure or figure_filename is not None

	grid, pieces = prepare_problem(filename)
	random.seed(seed)
	random.shuffle(pieces)

	# solver = solve_iter if use_iterative else solve_recursive
	solver = solve_recursive

	start = time.time()
	solver(grid, pieces, check_at=check_at)
	end = time.time()
	print(f"Solved in: {end - start:.2f} seconds")


	fig, ax = plt.subplots(1, 1, figsize=(6, 6))
	grid.draw(ax=ax)
	ax.set(xlim=(2, 23), ylim=(-3, 18))
	ax.set_aspect("equal")
	plt.axis("off")
	plt.tight_layout()

	if save_figure:
		plt.savefig(figure_filename)
	
	if save_solution:
		with open(filename, "r") as fp:
			problem_conf = yaml.safe_load(fp)
			assert "solution" not in problem_conf, "Solution already exists"

		solution  = {
			piece.index: {
				"x": piece.base_x,
				"y": piece.base_y,
				"rotation": piece.rotation,
			}
			for piece in pieces
		}
		with open(filename, "a") as fp:
			yaml.safe_dump({"solution": solution}, fp)

	plt.show()


if __name__ == "__main__":
	solve(
		filename="problems/9_pieces_v2.yaml",
		seed=42,
		check_at=3,
		save_solution=True,
	)
