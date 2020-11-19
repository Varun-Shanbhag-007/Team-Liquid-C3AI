## Model
This folder consists of python files that retrieve the data from c3aidatalake, preprares it and calculates w, alpha and beta parameters needed for the simulation. 

### param
This file implemented the parameter estimation algorithm suggeseted in Calafiore, Novara, and Possieri (2020), which simulated a modified SIR model for Italy cities. It first gets the county data and time period from calc_delta.py, then does all the caluclations, and generate an output file with counties, time periods and the estimated parameters during those time periods.
### get_county_params
This function collects the county's data from get_simulation_data in preparedata.py
### loss_function, calculate_Phi
Support functions to run the parameter estimation party

### cal_delta
#### get_county_data
Using an input file with the counties of interest, the function reformat the county into a standard format that c3aidatalake.py accepts.
#### get_time_period
Given the parameter estimation done in different time periods, this file runs the time delta calculation with start date, time interval, and number of iterations manually.

## Usage in this project
The estimated parameters are used in simulation.py in the Animation directory

## Reference
Calafiore, G. C., Novara, C., and Possieri, C. (2020) A Modified SIR Model for the COVID-19 Contagion in Italy. arXiv.org. Retrieved from https://arxiv.org/pdf/2003.14391.pdf 