from person import Person
from utils import Status
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#SIMULATION PARAMETERS
n = 10  #Population size
infected_percent = 50  #percentage of infected people at the beginning of the simulation (0-100%)
infection_radius=5  #radius of transmission in pixels (0-100)
contraction_probability=50  #probability of transmission in percentage (0-100%)
# p_aislamiento = 70  #percentage of the people in quarantine (0-100%)
recovery_time=200   #time taken to recover in number of frames (0-infinity)

population = []
currently_infected = 0
people_to_infect = n * infected_percent/100

for i in range(n):

    if i < people_to_infect:
        p = Person(i, (np.random.random()*100, np.random.random()*100), Status.INFECTED)
    else:
        p = Person(i, (np.random.random()*100, np.random.random()*100), Status.SUSCEPTIBLE)

    population.append(p)

print(population)