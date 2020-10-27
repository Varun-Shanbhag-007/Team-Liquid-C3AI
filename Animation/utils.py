from enum import Enum
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