# A* Implementation
# By Emet Behrendt

import random

import numpy as np

# S for start
# E for end
# ' ' for empty
# O for big obsticle (Blocks path)
# o for small obsticle (Slows path)
# x for path
GRID = (('.', '.', '.', '.', '.', '.', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.', 'O', '.', '.', 'E'), 
		('.', '.', '.', '.', '.', '.', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.', 'O', '.', '.', '.'),
		('.', 'O', '.', '.', '.', '.', '.', 'O', '.', '.', '.', '.', 'O', '.', '.', '.', 'O', '.', '.', '.'),
		('.', 'O', '.', '.', '.', '.', '.', 'O', '.', 'o', 'o', 'o', 'O', '.', '.', '.', 'O', '.', '.', '.'),
		('.', 'O', '.', '.', '.', 'O', '.', 'O', '.', '.', '.', '.', 'O', '.', '.', '.', 'O', 'O', '.', '.'),
		('.', 'O', 'O', 'O', '.', 'O', '.', 'O', '.', '.', '.', '.', 'O', '.', '.', '.', '.', 'o', '.', '.'),
		('.', '.', 'O', '.', '.', 'O', '.', 'O', '.', '.', '.', '.', 'O', '.', 'O', '.', '.', '.', '.', '.'),
		('.', '.', 'O', '.', '.', 'O', '.', 'O', '.', '.', '.', '.', '.', '.', 'O', '.', '.', '.', '.', '.'),
		('.', '.', '.', '.', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.', 'O', '.', 'O', 'O', 'O', 'O'),
		('.', '.', '.', '.', '.', 'O', '.', '.', 'O', 'O', 'O', 'O', '.', '.', 'O', '.', '.', '.', '.', '.'),
		('.', '.', '.', '.', '.', 'O', '.', '.', '.', '.', '.', 'O', 'o', 'o', 'O', '.', '.', '.', '.', '.'),
		('.', '.', '.', '.', '.', 'O', '.', 'O', 'O', '.', '.', 'O', '.', '.', 'O', '.', '.', '.', '.', '.'),
		('.', '.', '.', '.', '.', 'O', '.', '.', 'O', 'O', '.', 'O', '.', '.', 'O', '.', '.', '.', '.', '.'),
		('.', '.', 'o', '.', '.', 'O', '.', '.', '.', 'O', '.', 'O', '.', '.', 'O', '.', '.', '.', '.', '.'),
		('.', '.', 'O', '.', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.', 'O', 'O', 'O', '.', '.', '.'),
		('.', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'),
		('.', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.', 'O', 'O', 'O', '.', '.', '.', '.', '.', '.'),
		('.', '.', 'O', '.', '.', '.', '.', 'O', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'),
		('.', '.', 'O', '.', '.', '.', '.', '.', 'O', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'),
		('S', '.', 'O', '.', '.', '.', '.', '.', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'),
		)

# Cost of walking one tile horizontal or vertical
CARDINAL_COST = 10
# Cost of walking one tile diagonal
DIAGONAL_COST = 14
# Added cost of walking on obsticle node 
OBSTICLE_COST = 30

# Path class
# Used for storage of movement values
class Path:
	def __init__(self):
		# Creates a list to store path movements
		self.path = []

	# Returns number of path movements
	def __len__(self):
		print(len(self.path))

	# Prints path movements
	def __str__(self):
		print(self.path)

	# Adds a movement to the path
	def add(self, direction):
		self.path.append(direction)

	# Pastes the path on a grid object
	def paste(self, grid):
		grid = list(grid)

		# --- Finds the Start Position ---
		start_pos = []
		exit = False
		# Loops through each node in grid
		for i_row in range(len(grid)):
			for i_col in range(len(grid[i_row])):
				# Checks if the node is start position
				if grid[i_col][i_row] == 'S':
					start_pos = [i_row, i_col]
					exit = True
					break
			if exit:
				break

		pos = list(start_pos)
		# Loops through path movements
		for direction in self.path:
			# Updates position based on path movement
			if direction == 'U':
				pos[1] += -1
			elif direction == 'R':
				pos[0] += 1
			elif direction == 'D':
				pos[1] += 1
			elif direction == 'L':
				pos[0] += -1

			# Update node value
			grid[pos[1]][pos[0]] = 'x'

		return grid

	# Displays the path on passed grid
	def show(self, grid):
		grid = __class__.paste(grid)

		for row in grid:
			print(*row, sep='') 

# Nodes class
# Used for storage node type, location, cost value, and list of connected nodes
class Node():
	def __init__(self):
		self.is_start = False
		self.is_end = False
		self.walkable = True
		self.type = '.'
		self.x = 0
		self.y = 0
		self.e = 0		# Elevation of node
		self.f_cost = 0
		self.g_cost = 0		# Distance from start node
		self.h_cost = 0		# Distance from end node
		self.last = None
		self.connected = set()

	# Returns distance between two nodes
	def distance_to(self, node):
		dx = abs(self.x-node.x)
		dy = abs(self.y-node.y)

		dist = 10*abs(dx-dy)
		dist += 14*min(dx, dy)

		return dist

	@staticmethod
	# Calculates F cost
	def calc_f_cost(origin, destination, end):
		# G cost + H cost
		return __class__.calc_g_cost(origin, destination) + __class__.calc_h_cost(origin, end)

	# Calculates g cost
	@staticmethod
	def calc_g_cost(origin, destination):
		return origin.g_cost + __class__.distance(origin, destination) + destination.e

	# Calculates h cost
	@staticmethod
	def calc_h_cost(origin, end):
		return __class__.distance(origin, end)

	# Calculates distance between two nodes
	@staticmethod
	def distance(node, node2):
		dx = abs(node.x-node2.x)
		dy = abs(node.y-node2.y)

		dist = 10*abs(dx-dy)
		dist += 14*min(dx, dy)

		return dist

# Grid class
# Stores 2d array of nodes based on 2d array of values
class Grid:
	def __init__(self, grid):
		self.grid = grid
		self.solved_grid = None
		self.path = Path()
		self.coord_path = []
		self.solved = False
		self.node_grid = []
		self.start = Node()
		self.end = Node()

		# Fills 2d array with nodes
		for i in range(len(grid)):
			self.node_grid.append([])
			for j in range(len(grid[i])):
				self.node_grid[i].append(Node())

		# Reads passed grid and store values in nodes array
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				for k in range(-1, 2):
					for l in range(-1, 2):
						if k != 0 or l != 0:
							try:
								if (i + k) >= 0 and (j + l) >= 0:
									self.node_grid[i][j].connected.add(self.node_grid[i + k][j + l])
							except IndexError:
								pass

				self.node_grid[i][j].type = grid[i][j]

				self.node_grid[i][j].x = j
				self.node_grid[i][j].y = i

				if self.node_grid[i][j].type != '.' and self.node_grid[i][j].type != ' ':
					if grid[i][j] == 'O':
						self.node_grid[i][j].walkable = False
					elif grid[i][j] == 'o':
						self.node_grid[i][j].e += OBSTICLE_COST
					# Sets start and end node
					elif grid[i][j] == 'S':
						self.start = self.node_grid[i][j]
						self.node_grid[i][j].is_start = True
					elif grid[i][j] == 'E':
						self.end = self.node_grid[i][j]
						self.node_grid[i][j].is_end = True

	# Updates the grid with a solved path
	def a_star(self):
		opened = []
		closed = set()

		opened.append(self.start)

		while True:
			if len(opened) == 0:
				raise BaseException("Error. No path could be found.")

			lowest_index = 0
			for n_index in range(1, len(opened)):
				if opened[n_index].f_cost < opened[lowest_index].f_cost:
					lowest_index = n_index

			# Store current node in temp variable and remove node from open list
			current_node = opened[lowest_index]
			opened.remove(current_node)
			closed.add(current_node)

			# Checks if the end node has been found
			if current_node.is_end:
				while True:
					current_node.type = 'x'

					if current_node.is_start:
						break
					else:
						current_node = current_node.last

				self.solved = True
				return self.path

			highest_index = 0
			for connected_node in current_node.connected:
				# If in open list
				if connected_node in opened:
					updated_g_cost = Node.calc_g_cost(current_node, connected_node)
					if connected_node.g_cost > updated_g_cost:
						connected_node.g_cost = updated_g_cost
						connected_node.f_cost = Node.calc_f_cost(current_node, connected_node, self.end)
						connected_node.last = current_node
				# If not in open list and not in closed list
				elif connected_node not in closed and connected_node.walkable:
					connected_node.last = current_node
					connected_node.g_cost = Node.calc_g_cost(current_node, connected_node)
					connected_node.f_cost = Node.calc_f_cost(current_node, connected_node, self.end)
					opened.append(connected_node)

	# Displays the grid
	def show(self):
		for row in self.grid:
			print(*row, sep=' ') 

	# Prints solved grid
	def show_solved(self):
		if self.solved:
			for i in range(len(self.node_grid)):
				for j in range(len(self.node_grid[i])):
					print(self.node_grid[i][j].type, end=' ')
				print()		# New line

		else:
			print("Grid is unsolved. Use Grid solve method to solve.")

# Main Function
def main():
	height = 20
	width = 20

	grid = Grid(GRID)

	print("\nUnsolved Grid:")
	grid.show()
	print("\nSolved Grid:")
	grid.a_star()
	grid.show_solved()

	# Prints node values
	'''
	print("\nGrid with Values:")
	for i in range(len(grid.node_grid)):
		for j in range(len(grid.node_grid[i])):
			print(grid.node_grid[i][j].g_cost, '\t', end='')
		print()
	'''

if __name__ == "__main__":
	main()
