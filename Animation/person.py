class Person:

    def __init__(self, i, home_coords, status):

        self.idx = i

        self.home_x, self.home_y = home_coords

        self.x, self.y = home_coords

        self.status = status
        self.infected_time = -1

        self.is_quarantined = False

        self.speed = 1

    def get_current_position(self):
        return (self.x, self.y)

    def quarantine(self, action):
        self.is_quarantined = action

    def __repr__(self):
        return("Person " + str(self.idx) +" -> "+ str(self.status) + " @ " + str(self.x) +" , "+ str(self.y))

    

    