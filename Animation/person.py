from utils import astar
import numpy as np


class Person:

    def __init__(self, i, home_coords, status):

        self.idx = i

        self.home_x, self.home_y = home_coords

        self.x, self.y = home_coords

        self.status = status
        self.infected_time = -1

        self.is_quarantined = False

        self.velocity = 1
        self.dest_x, self.dest_y = home_coords
        self.movement = []
        self.day_infected = -1


    def get_current_position(self):
        return (self.x, self.y)


    def quarantine(self, action):
        self.is_quarantined = action


    def make_up_mind(self, entries, matrix):
        # print("Making mind for", self)
        dest = (np.random.choice(4, 1, p=[0.5, 0.2, 0.2, 0.1]))[0]

        if dest != 0:
            self.movement = astar(matrix,int(self.x),int(self.y), entries[dest-1][0], entries[dest-1][1])
        else:
            self.movement = astar(matrix,int(self.x),int(self.y), int(self.home_x), int(self.home_y))

        if len(self.movement) == 1:
            self.movement = [self.movement[0]]*100


    def __repr__(self):
        return("Person " + str(self.idx) +" -> "+ str(self.status) + " @ " + str(self.x) +" , "+ str(self.y) + "\n")