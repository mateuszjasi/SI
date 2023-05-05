import sys

import maze_puzzle as mp
from random import randrange


# Function to find a route using the Depth-first Search algorithm.

# Depth-first search is an algorithm used to traverse a tree or generate nodes and paths in a tree. This algorithm
# starts at a specific node and explores paths of connected nodes of the first child and does this recursively until
# it reaches the furthest leaf node before backtracking and exploring other paths to leaf nodes via other child nodes
# that have been visited.

# Although the Depth-first search algorithm van be implemented with a recursive function. This implementation is
# achieved using a stack to better represent the order of operations as to which nodes get visited and processed.
# It is important to keep track of the visited points so that the same nodes do not get visited unnecessarily and
# create cyclic loops.

def run_dfs(maze_puzzle, current_point, visited_points):
    visited_points.append(current_point)
    neighbors = maze_puzzle.get_neighbors(current_point)
    for neighbor in neighbors:
        if not is_in_visited_points(neighbor, visited_points):
            neighbor.set_parent(current_point)
            if maze_puzzle.get_current_point_value(neighbor) == '*':
                return neighbor
            w = run_dfs(maze_puzzle, neighbor, visited_points)
            if w != 'No path to the goal found.':
                return w
    return 'No path to the goal found.'


# Function to determine if the point has already been visited
def is_in_visited_points(current_point, visited_points):
    for visited_point in visited_points:
        if current_point.x == visited_point.x and current_point.y == visited_point.y:
            return True
    return False


sys.setrecursionlimit(3000)
print('---Depth-first Search---')
n = int(input('Podaj długość boku labirytnu: '))
# Initialize a MazePuzzle
maze_game_main = mp.MazePuzzle(n, n)

# Run the depth first search algorithm with the initialized maze
starting_point = mp.Point(0, randrange(n))
outcome = run_dfs(maze_game_main, starting_point, [])

# Get the path found by the depth first search algorithm
dfs_path = mp.get_path(outcome)

# Print the results of the path found
print('Path Length: ', len(dfs_path))
maze_game_main.overlay_points_on_map(dfs_path)
print('Path Cost: ', mp.get_path_cost(outcome))
for point in dfs_path:
    print('Point: ', point.x, ',', point.y)
