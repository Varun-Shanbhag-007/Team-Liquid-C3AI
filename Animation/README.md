## Simulation/Animation
This folder consists of python files that retrieve the data from model(w,beta) and perform a randomized simulation to effectively predict the rate of infection across given county



_Note_ : There are 2 branches to be used here. 

-   The `simulation` on this file simulates under `main` branch is our proposed solution.
-   The `simulation.py` under the `Normal` branch is the situation under the normal situation with parameters estimated from the data-lake.

## File Descriptions

**simulation.py** : This is the main file that runs the simulation. Simply run `python simulation.py`. All the variables have been set. The code first generates a population and then runs the simulation, while plotting the SIR graph simultaneously.

<br>

**person.py** : This is a file containing the class of a single `Person`. Objects of this class are used to build the population in the `simulation.py` file. It contains information about the person's home location, COVID score (`score`) etc.

<br>

**utils.py** : This file has some utility files that have the pathfinding algorithms mainly amongst some other Enums that are used in the other file.

<br>

**plot.py** : Simple file to plot the final combined graph of the normal lines and the solution lines.



## Usage

As mentioned, to run, simply run `python simulation.py`. This will generate a csv file so that data is not needed to generate in the future runs.

If a csv file is present, run `python simulation.py 123` to use the data present there.