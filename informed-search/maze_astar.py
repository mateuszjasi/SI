from collections import deque
from random import randrange

import maze_puzzle as mp


# Function to find a route using A* Search algorithm.

# The A* algorithm usually improves performance by estimating heuristics to minimize cost of the next node visited.
# Total cost is calculated using two metrics: the total distance from the start node to the current node, and the
# estimated cost of moving to a specific node by utilizing a heuristic. When attempting to minimize cost, a lower
# value will indicate a better performing solution.
def run_astar(maze_game, current_point, visited_points):
    # TODO: Dla podstawowej postaci labiryntu wynik powinien być identyczny jak w BFS.
    queue = [current_point]
    while queue:
        current_point = queue.pop()
        if not is_in_visited_points(current_point, visited_points):
            visited_points.append(current_point)
            if maze_game.get_current_point_value(current_point) == '*':
                return current_point
            else:
                neighbors = maze_game.get_neighbors(current_point)
                for neighbor in neighbors:
                    neighbor.set_parent(current_point)
                    neighbor.set_cost(determine_cost(current_point, neighbor))
                    queue.append(neighbor)
                queue.sort(key=lambda x: x.cost, reverse=True)
    return "No path to the goal found"


# Determine cost based on the distance to root
def determine_cost(current_point, neighbor):
    #TODO
    return mp.get_path_length(neighbor) + mp.get_move_cost(current_point, neighbor)


# Function to determine if the point has already been visited
def is_in_visited_points(current_point, visited_points):
    for visited_point in visited_points:
        if current_point.x == visited_point.x and current_point.y == visited_point.y:
            return True
    return False


print('---A* Search---')
n = int(input('Podaj długość boku labirytnu: '))
# Function to determine if the point has already been visited
maze_game_main = mp.MazePuzzle(n, n)

# Run the greedy search algorithm with the initialized maze
starting_point = mp.Point(0, randrange(n))
outcome = run_astar(maze_game_main, starting_point, [])

# Get the path found by the greedy search algorithm
astar_path = mp.get_path(outcome)

# Print the results of the path found
print('PATH LENGTH: ', mp.get_path_length(outcome))
maze_game_main.overlay_points_on_map(astar_path)
print('PATH COST: ', mp.get_path_cost(outcome))
for point in astar_path:
    print('Point: ', point.x, ',', point.y)
