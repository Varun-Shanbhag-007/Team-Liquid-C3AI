from person import Person
from utils import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

squares= [[0,0,20,20],[40,40,60,60],[80,80,100,100]]
entries = [(10,20), (50, 60), (90, 80)]



matrix = []
x = 101
y = 101

for i in range(x):
    temp=[]
    for j in range(y):
        if((i>=0 and i<20) and (j>=0 and j<20)):
            temp.append(0)
        elif((i>=40 and i<60) and (j>=40 and j<60)):
            temp.append(0)
        elif((i>=80 and i<100) and (j>=80 and j<100)):
            temp.append(0)
        else:
            temp.append(1)        
    matrix.append(temp)


#SIMULATION PARAMETERS
scale = 100
n = 10000  #Population size
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

    p.make_up_mind(entries)

    population.append(p)

print(population)
fig = plt.figure(figsize=(18,18))
ax = fig.add_subplot(111) 

ax.add_patch(patches.Rectangle((0,0),scale/5,scale/5,fill=False))
ax.add_patch(patches.Rectangle((40,40),scale/5,scale/5,fill=False))
ax.add_patch(patches.Rectangle((80,80),scale/5,scale/5,fill=False))

scatt = ax.scatter([person.x for person in population], [person.y for person in population], s=4, c=[return_color(person.status.value) for person in population])
print("************")
print("ALL PLOTTED")

def update(frame):
    print("UPDATING")
    for person in population:
        if person.movement == []:
            person.make_up_mind(entries)
        
        next_step = person.movement.pop()
        person.x = next_step[0]
        person.y = next_step[1]

        if(person.x > scale):
            person.x = scale
        if(person.x < 0):
            person.x = 0
        if person.y > scale:
            person.y = scale
        if person.y < 0:
            person.y = 0

    offsets = np.array([[person.x for person in population], [person.y for person in population]])
    scatt.set_offsets(np.ndarray.transpose(offsets))
    return scatt,

animation = FuncAnimation(fig, update, blit=True, interval=25)
plt.show()

    