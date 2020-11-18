import matplotlib.pyplot as plt
from numpy.matrixlib.defmatrix import bmat
import pandas as pd


def plot_difference(currently_infected_sol, currently_infected_b_closed, currently_infected_normal):

    time = list(range(1, 4005))
    fig = plt.figure(figsize=(18, 18))
    cx = fig.add_subplot()
    cx.axis([-100, 4000, -10, 3000])
    c_inf_plt, = cx.plot(currently_infected_sol, color="red",
                         label="Infected during Solution", linestyle='dashed')
    c_inf_plt_n, = cx.plot(currently_infected_normal, color="red",
                           label="Infected during B_Closed")
    c_inf_plt_b_closed, = cx.plot(currently_infected_b_closed, color="red",
                                  label="Infected during B Closed", linestyle='dashdot')

    cx.legend(handles=[c_inf_plt, c_inf_plt_n, c_inf_plt_b_closed])
    cx.fill_between(time, currently_infected_normal,
                    currently_infected_sol, facecolor='g', alpha=0.5)
    cx.set_xlabel("Time")
    cx.set_ylabel("People")

    plt.show()


def plot_all(currently_suseptible_sol, currently_infected_sol, currently_recovered_sol, currently_suseptible_b_closed, currently_infected_b_closed, currently_recovered_b_closed):
    time = list(range(1, 4005))
    fig = plt.figure(figsize=(18, 18))
    cx = fig.add_subplot()
    cx.axis([-100, 4000, -10, 3000])
    c_sus_plt, = cx.plot(currently_suseptible_sol,
                         color="blue", label="Suseptible_Sol", linestyle='dashed')
    c_inf_plt, = cx.plot(currently_infected_sol, color="red",
                         label="Infected during Solution", linestyle='dashed')
    c_rec_plt, = cx.plot(currently_recovered_sol,
                         color="gray", label="Recovered_Sol", linestyle='dashed')
    c_sus_plt_b, = cx.plot(currently_suseptible_b_closed,
                           color="blue", label="Suseptible B_Closed", )
    c_inf_plt_b, = cx.plot(currently_infected_b_closed, color="red",
                           label="Infected during B_Closed")
    c_rec_plt_b, = cx.plot(currently_recovered_b_closed,
                           color="gray", label="Recovered B_Closed")

    cx.legend(handles=[c_sus_plt, c_inf_plt, c_rec_plt,
                       c_sus_plt_b, c_inf_plt_b, c_rec_plt_b])

    cx.set_xlabel("Time")
    cx.set_ylabel("People")
    plt.show()


#############___MAIN___#################

df_norm = pd.read_csv('C3AI\Results\\Normal.csv', header=None)
df_sol = pd.read_csv('C3AI\Results\Sol_.5_1_.8.csv', header=None)
df_b_closed = pd.read_csv('C3AI\Results\Sol_Only_B_Closed.csv', header=None)

currently_suseptible_norm = df_norm[0]
currently_infected_norm = df_norm[1]
currently_recovered_norm = df_norm[2]


currently_suseptible_b_closed = df_b_closed[0]
currently_infected_b_closed = df_b_closed[1]
currently_recovered_b_closed = df_b_closed[2]

currently_suseptible_sol = df_sol[0]
currently_infected_sol = df_sol[1]
currently_recovered_sol = df_sol[2]

print()

norm_infection = 3000 - currently_suseptible_norm.iloc[-1]
sol_infection = 3000 - currently_suseptible_sol.iloc[-1]
b_closed_infection = 3000 - currently_suseptible_b_closed.iloc[-1]

print(f"Infected with Normal {norm_infection}")
print(f"Infected with B-Closed Solution {b_closed_infection}")
print(f"Infected with Implemented Solution {sol_infection}")

print(
    f"Solution drops infection rate by {(norm_infection-sol_infection)/norm_infection}")

plot_difference(currently_infected_sol,
                currently_infected_b_closed, currently_infected_norm)

# plot_all(currently_suseptible_sol, currently_infected_sol, currently_recovered_sol,
#          currently_suseptible_b_closed, currently_infected_b_closed, currently_recovered_b_closed)
