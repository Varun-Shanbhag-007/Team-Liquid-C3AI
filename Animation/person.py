from utils import *
import numpy as np
import random
import copy


class Person:

    def __init__(self, i, home_coords, status, entries, matrix, roads):

        self.idx = i

        self.home_x, self.home_y = home_coords
        self.x, self.y = copy.deepcopy(home_coords)
        self.home_coords = (self.home_x, self.home_y)
        self.curr_coords = (self.x, self.y)
        self.road_to_home = {}
        self.road_to_home[Destination.LOC_A] = astar(
            matrix, entries[0][0], entries[0][1], self.home_x, self.home_y)  # Loc A
        self.road_to_home[Destination.LOC_B] = astar(
            matrix, entries[1][0], entries[1][1], self.home_x, self.home_y)  # Loc B
        self.road_to_home[Destination.LOC_C] = astar(
            matrix, entries[2][0], entries[2][1], self.home_x, self.home_y)  # Loc C
        self.roads = roads

        self.status = status

        self.quarantine_in_frames = random.randint(1, 1000)

        self.is_quarantined = False

        self.velocity = 1
        self.dest_x, self.dest_y = home_coords
        self.dest = Destination.HOME
        self.movement = []

        self.frame_infected = -1
        self.random_walk = -1

    def get_current_position(self):
        return (self.x, self.y)

    def quarantine(self, action):
        self.is_quarantined = action

    def make_up_mind(self, entries, matrix):
        origin = self.dest
        dest = (np.random.choice(4, 1, p=[0.5, 0.2, 0.2, 0.1]))[0]

        if dest == 0:
            self.dest = Destination.HOME
        elif dest == 1:
            self.dest = Destination.LOC_A
        elif dest == 2:
            self.dest = Destination.LOC_B
        elif dest == 3:
            self.dest = Destination.LOC_C

        if self.dest == Destination.HOME and origin != Destination.HOME:
            self.movement = self.road_to_home[origin]
        elif self.dest != Destination.HOME and origin != Destination.HOME:
            self.movement = self.roads[findMyWay(origin, self.dest)]
        elif self.dest != Destination.HOME and origin == Destination.HOME:
            self.movement = list(reversed(self.road_to_home[self.dest]))
        elif self.dest == Destination.HOME and origin == Destination.HOME:  # home 2 home
            self.movement = [(self.home_x, self.home_y)]*100

        self.movement = copy.deepcopy(self.movement)

    def __repr__(self):
        return("Person " + str(self.idx) + " -> " + str(self.status) + " @ " + str(self.x) + " , " + str(self.y) + " dest = " + str(self.dest) + "\n")
