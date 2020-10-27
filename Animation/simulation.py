from person import Person
from utils import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

squares= [[0,0,200,200],[400,400,600,600],[800,800,1000,1000]]


#SIMULATION PARAMETERS
scale = 1000
n = 1000  #Population size
infected_percent = 50  #percentage of infected people at the beginning of the simulation (0-100%)
infection_radius=5  #radius of transmission in pixels (0-100)
contraction_probability=50  #probability of transmission in percentage (0-100%)
# p_aislamiento = 70  #percentage of the people in quarantine (0-100%)
recovery_time=200   #time taken to recover in number of frames (0-infinity)

population = []
currently_infected = 0
people_to_infect = n * infected_percent/100

for i in range(n):
    random_coords = (np.random.random()*scale, np.random.random()*scale)
    while(within(random_coords, squares)):
        random_coords = (np.random.random()*scale, np.random.random()*scale)
    
    if i < people_to_infect:
        p = Person(i, random_coords, Status.INFECTED)
    else:
        p = Person(i, random_coords, Status.SUSCEPTIBLE)

    population.append(p)

print(population)
fig = plt.figure(figsize=(18,18))
ax = fig.add_subplot(111) 

ax.add_patch(patches.Rectangle((0,0),scale/5,scale/5,fill=False))
ax.add_patch(patches.Rectangle((400,400),scale/5,scale/5,fill=False))
ax.add_patch(patches.Rectangle((800,800),scale/5,scale/5,fill=False))

plt.scatter([person.x for person in population], [person.y for person in population], s=4, c=[return_color(person.status.value) for person in population])
plt.show()