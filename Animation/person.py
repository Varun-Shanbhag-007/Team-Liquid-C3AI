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

    def get_current_position(self):
        return (self.x, self.y)

    def quarantine(self, action):
        self.is_quarantined = action

    def make_up_mind(self, entries):
        dest = (np.random.choice(4, 1, p=[0.5, 0.2, 0.2, 0.1]))

        if dest != 0:
            self.movement = astar(p.x,p.y, entries[dest-1][0], entries[dest-1][1])
        else:
            self.movement = [(p.x, p.y)]*100


    def __repr__(self):
        return("Person " + str(self.idx) +" -> "+ str(self.status) + " @ " + str(self.x) +" , "+ str(self.y) + "\n")

    

    