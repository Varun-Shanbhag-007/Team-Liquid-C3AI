from person import Person
from utils import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
from sys import argv
import pickle
from scipy.stats import rankdata

squares = [[0, 0, 21, 21], [39, 39, 61, 61], [79, 79, 100, 100]]

matrix = []
x = 101
y = 101

entries = [(10, 21), (50, 61), (90, 79)]
inside_entries = [(10, 19), (50, 59), (90, 81)]
random_walk_time = 20

for i in range(x):
    temp = []
    for j in range(y):
        if((i >= 0 and i <= 20) and (j >= 0 and j <= 20)):
            temp.append(0)
        elif((i >= 40 and i <= 60) and (j >= 40 and j <= 60)):
            temp.append(0)
        elif((i >= 80 and i <= 100) and (j >= 80 and j <= 100)):
            temp.append(0)
        else:
            temp.append(1)
    matrix.append(temp)

for entry in entries:
    matrix[entry[0]][entry[1]] = 1

roads = {}
roads["AB"] = astar(matrix, entries[0][0], entries[0]
                    [1], entries[1][0], entries[1][1])
roads["BC"] = astar(matrix, entries[1][0], entries[1]
                    [1], entries[2][0], entries[2][1])
roads["CA"] = astar(matrix, entries[2][0], entries[2]
                    [1], entries[0][0], entries[0][1])
roads["BA"] = list(reversed(roads["AB"]))
roads["CB"] = list(reversed(roads["BC"]))
roads["AC"] = list(reversed(roads["CA"]))
roads["AA"] = [entries[0]]
roads["BB"] = [entries[1]]
roads["CC"] = [entries[2]]


# SIMULATION PARAMETERS
scale = 100
n = 3000  # 3169  # Population size 85% scaled down p ka 0.05 susceptible

# percentage of infected people at the beginning of the simulation (0-100%)
infected_percent = 0.02  # 893

infection_radius = 0.04  # radius of transmission in pixels (0-100)

# probability of transmission in percentage (0-100%)
contraction_probability = 0.0064 * 4

population = []
currently_infected = 0
currently_suseptible = 0
currently_recovered = 0
day = 0
iteration = 0
people_to_infect = n * infected_percent


try:
    if argv[1] != None:
        population = pickle.load(open('save_file1.dat', "rb"))

    for person in population:
        if person.status == Status.INFECTED:
            currently_infected += 1
        elif person.status == Status.SUSCEPTIBLE:
            currently_suseptible += 1

except:
    for i in tqdm(range(n)):
        random_coords = (int(np.random.random()*scale),
                         int(np.random.random()*scale))
        while(within(random_coords, squares)):
            random_coords = (int(np.random.random()*scale),
                             int(np.random.random()*scale))

        if i < people_to_infect:
            p = Person(i, random_coords, Status.INFECTED,
                       entries, matrix, roads)
            currently_infected += 1
            p.day_infected = 0
            p.score = 100
        else:
            p = Person(i, random_coords, Status.SUSCEPTIBLE,
                       entries, matrix, roads)
            currently_suseptible += 1

        p.make_up_mind(entries, matrix)

        population.append(p)
    print("Creating new DAT file")
    pickle.dump(population, open('save_file1.dat', "wb"))

fig = plt.figure(figsize=(18, 18))
ax = fig.add_subplot(121)
ax.add_patch(patches.Rectangle((0, 0), scale/5, scale/5, fill=False))
ax.add_patch(patches.Rectangle((40, 40), scale/5, scale/5, fill=False))
ax.add_patch(patches.Rectangle((80, 80), scale/5, scale/5, fill=False))

scatt = ax.scatter([person.x for person in population], [person.y for person in population], s=4, c=[
                   return_color(person.status.value) for person in population])

sir_graph = plt.Rectangle((0, 0), 100, 100, fill=False)
ax.add_patch(sir_graph)


cx = fig.add_subplot(122)
cx.axis([-100, 4000, -10, n])
c_sus_plt, = cx.plot(currently_suseptible, color="blue", label="Suseptible")
c_inf_plt, = cx.plot(currently_infected, color="red",
                     label="Currently infected")
c_rec_plt, = cx.plot(currently_recovered, color="gray", label="Recovered")

cx.legend(handles=[c_sus_plt, c_inf_plt, c_rec_plt])
cx.set_xlabel("Time")
cx.set_ylabel("People")

cs = [currently_suseptible]
ci = [currently_infected]
cr = [0]
t = [0]


def check_dest(dest):
    global population
    score_at_dest = 0
    for person in population:
        if person.dest == dest and person.status == Status.INFECTED:
            score_at_dest += person.score
    return score_at_dest


FRAMES_NUM = 4000


def update(frame, cs, ci, cr, t):
    global day, iteration, currently_infected, currently_recovered, currently_suseptible, contraction_probability

    if frame == FRAMES_NUM:
        columns = {}
        columns['S'] = cs
        columns['I'] = ci
        columns['R'] = cr
        data = list(zip(columns['S'], columns['I'], columns['R']))
        df = pd.DataFrame(data=data)
        df.to_csv('SIR.csv', index=False, header=False)
        print(f'{frame} == {FRAMES_NUM}; closing!')
        return scatt, c_sus_plt, c_inf_plt, c_rec_plt
    else:
        prior_to_infection = 0
        count = 1

        inf_a, inf_b, inf_c = 0, 0, 0
        at_a, at_b, at_c = 0, 0, 0
        mobile_people = 0
        for person in population:

            if person.is_quarantined == False:
                mobile_people += 1
            if person.status == Status.INFECTED:
                if person.dest == Destination.LOC_A:
                    inf_a += 1
                elif person.dest == Destination.LOC_B:
                    inf_b += 1
                elif person.dest == Destination.LOC_C:
                    inf_c += 1
            if person.dest == Destination.LOC_A:
                at_a += 1
            if person.dest == Destination.LOC_B:
                at_b += 1
            if person.dest == Destination.LOC_C:
                at_c += 1
        inf_counts = list(
            np.array([0, inf_a, inf_b, inf_c])/(inf_a + inf_b + inf_c))
        distribution = list(np.array([0, at_a, at_b, at_c])/mobile_people)
        supposed_distribution = [0.5, 0.2, 0.2, 0.1]

        for person in population:

            if(person.is_quarantined):
                pass
            # Movement
            else:
                if len(person.movement) == 0:
                    if person.random_walk == 0:
                        person.x, person.y = entries[person.dest.value-1]
                        person.random_walk = -1

                    if person.random_walk == -1:
                        mind_made = False
                        while(not mind_made):
                            person.make_up_mind(entries, matrix)
                            if person.dest == Destination.HOME:
                                mind_made = True
                            else:
                                # more than avg?
                                if distribution[person.dest.value] > supposed_distribution[person.dest.value]:
                                    mind_made = False
                                else:
                                    if inf_counts[person.dest.value] == max(inf_counts):
                                        if(np.random.random() <= 0.5):
                                            mind_made = True
                                    elif inf_counts[person.dest.value] == min(inf_counts):
                                        mind_made = True
                                    else:
                                        if(np.random.random() <= 0.8):
                                            mind_made = True
                    else:
                        person.x += np.random.randint(-3, 4)
                        person.y += np.random.randint(-3, 4)
                        if(person.x > squares[person.dest.value-1][2]):
                            person.x = squares[person.dest.value-1][2]-1
                        if(person.x < squares[person.dest.value-1][0]):
                            person.x = squares[person.dest.value-1][0]
                        if person.y > squares[person.dest.value-1][3]:
                            person.y = squares[person.dest.value-1][3]-1
                        if person.y < squares[person.dest.value-1][1]:
                            person.y = squares[person.dest.value-1][1]
                        person.random_walk -= 1

                if len(person.movement) == 1:

                    if(person.dest == Destination.HOME):
                        pass
                    elif person.dest == Destination.LOC_A:
                        person.x, person.y = inside_entries[Destination.LOC_A.value-1]
                        person.random_walk = random_walk_time
                        person.movement.pop()
                    elif person.dest == Destination.LOC_B:
                        if person.status == Status.INFECTED:
                            person.make_up_mind(entries, matrix)

                        else:
                            person.x, person.y = inside_entries[Destination.LOC_B.value-1]
                            person.random_walk = random_walk_time
                            person.movement.pop()
                    elif person.dest == Destination.LOC_C:
                        person.x, person.y = inside_entries[Destination.LOC_C.value-1]
                        person.random_walk = random_walk_time
                        person.movement.pop()

                if person.random_walk == -1:
                    next_step = person.movement.pop(0)
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

                if frame % 10 == 0 and person.status == Status.INFECTED:
                    if person.x == person.home_x and person.y == person.home_y:
                        # He is at his own home. Cant spread.
                        pass
                    else:
                        for person2 in population:
                            if person2.status == Status.INFECTED or person2.status == Status.RECOVERED:
                                pass
                            else:
                                distance = np.sqrt((person2.x - person.x)
                                                   ** 2 + (person2.y - person.y)**2)
                                if distance <= infection_radius:
                                    if (person2.x, person2.y) == person2.home_coords:
                                        pass
                                    else:
                                        if np.random.random() <= contraction_probability:
                                            person2.status = Status.INFECTED
                                            person2.frame_infected = frame
                                            currently_infected += 1
                                            currently_suseptible -= 1
                                            prior_to_infection += person2.score
                                            count += 1
                                        else:
                                            person2.score += 1

            # Infection
            # 200 frame is 1 day
            if person.status == Status.INFECTED and frame - person.frame_infected >= person.quarantine_in_frames:
                person.x, person.y = person.home_coords
                person.is_quarantined = True

            # 200 frame is 1 day
            if person.status == Status.INFECTED and frame - person.frame_infected >= 1000:
                person.status = Status.RECOVERED
                person.is_quarantined = False
                currently_recovered += 1
                currently_infected -= 1

        # Day count
        iteration += 1
        if iteration == 200:
            day += 1
            iteration = 0
        # print("***")
        for person in population:
            if person.status == Status.SUSCEPTIBLE:
                person.score -= person.score/14

        # update the plotting data
        cs.append(currently_suseptible)
        ci.append(currently_infected)
        cr.append(currently_recovered)
        t.append(frame)

        offsets = np.array([[person.x for person in population], [
            person.y for person in population]])
        scatt.set_offsets(np.ndarray.transpose(offsets))
        scatt.set_color([return_color(person.status.value)
                         for person in population])
        c_sus_plt.set_data(t, cs)
        c_inf_plt.set_data(t, ci)
        c_rec_plt.set_data(t, cr)
        return scatt, c_sus_plt, c_inf_plt, c_rec_plt


animation = FuncAnimation(fig, update, blit=True,
                          interval=25, fargs=(cs, ci, cr, t))
plt.show()
