from enum import Enum
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Status(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2

class Destination(Enum):
    HOME = 0
    LOC_A = 1
    LOC_B = 2
    LOC_C = 3


def return_color(status_enum):
    if status_enum == 0 :
        return 'blue'
    elif status_enum == 1:
        return 'red'
    else:
        return 'cyan'


def within(point, squares):
    x, y = point
    for sq in squares:
        if x >= sq[0] and x<=sq[2]:
            if y >= sq[1] and y<=sq[3]:
                return True
    
    return False


def astar(matrix,x1,y1,x2,y2):
    grid = Grid(matrix = matrix)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(grid.node(x1,y1),grid.node(x2,y2), grid)
    return path

def closest_distance (healthy,infected,infected_index):
    lst = np.array([[ np.linalg.norm(i-j) for j in infected] for i in healthy])
    df = pd.DataFrame(lst, columns = infected_index)
    return df
