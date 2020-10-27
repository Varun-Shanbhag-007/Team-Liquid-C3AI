from enum import Enum
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Status(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2

def return_color(x):
    print(x)
    if x == 0 :
        return 'blue'
    elif x == 1:
        return 'red'
    else:
        return 'yellow'

def within(point, squares):
    
    x, y = point

    for sq in squares:
        if x >= sq[0] and x<=sq[2]:
            if y >= sq[1] and y<=sq[3]:
                return True

    return False



def getPath(matrix,x1,y1,x2,y2):
    grid = Grid(matrix = matrix)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(grid.node(x1,y1),grid.node(x2,y2), grid)

    return path