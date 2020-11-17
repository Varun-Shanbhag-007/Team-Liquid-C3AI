import numpy as np
import numpy.linalg as la
from preparedata import get_simulation_data
import calc_delta
import csv

# Initializing variables needed for calculation
r_confirmed_cases, r_confirmed_deaths, r_confirmed_recoveries, r_infection_rate, r_mortality_rate, r_recovery_rate, \
    r_county_pop, r_county_pop_density, r_prob_visiting_grocery_store, r_prob_visiting_restaurant, \
    r_prob_visiting_park = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

infection_margin = 0
mortality_margin = 0
recovery_margin = 0


# This function returns the mean error for w and a
def loss_function(delta, phi, param):
    mse = (la.norm(delta-np.dot(phi, param), 2))**2
    return mse


# This function returns the phi value
def calculate_Phi(s, i, alpha):
    phi = np.array([[s*i/(s+i), -i, -alpha*i], [0, i, 0], [0, 0, i]])
    return phi


# This function returns the number of cases, recoveries, deaths and other parameters for a county.
# It takes the county name, start date and end date as parameters and returns these values from the 
# John Hopkins University: COVID-19 Data Repository using the get_simulation_data() function in preparedata.py
def get_county_params(county_name, time_range_1, time_range_2):
        r_confirmed_cases, r_confirmed_deaths, r_confirmed_recoveries, r_infection_rate, r_mortality_rate, \
        r_recovery_rate, r_county_pop, r_prob_visiting_grocery_store, r_prob_visiting_restaurant, r_prob_visiting_park \
            = get_simulation_data(county_name, time_range_1, time_range_2)

        infection_margin = [round(r_infection_rate[i]-r_infection_rate[i-1], 6) for i in range(1, len(r_infection_rate)-1)]

        mortality_margin = [round(r_mortality_rate[i]-r_mortality_rate[i-1], 6) for i in range(1, len(r_mortality_rate)-1)]

        recovery_margin = [round(r_recovery_rate[i]-r_recovery_rate[i-1], 6) for i in range(1, len(r_recovery_rate)-1)]
        return (r_confirmed_cases, r_confirmed_deaths, r_confirmed_recoveries, r_infection_rate, r_mortality_rate,
                r_recovery_rate, r_county_pop, r_county_pop_density, r_prob_visiting_grocery_store,
                r_prob_visiting_restaurant, r_prob_visiting_park, infection_margin, mortality_margin, recovery_margin,)


# Running the parameter calculation (Arika's code) for every county and every 2 week time period
final_copy_row = []
county_list = calc_delta.get_county_list()
print(county_list)
for curr_county in range(len(county_list)):
    timeperiod_1, timeperiod_2 = calc_delta.get_time_period()
    for time_index in range(len(timeperiod_1)):
        a = get_county_params(county_list[curr_county], timeperiod_1[time_index], timeperiod_2[time_index])
        r_confirmed_cases = a[0]
        r_confirmed_deaths = a[1]
        r_confirmed_recoveries = a[2]
        r_infection_rate = a[3]
        r_mortality_rate = a[4]
        r_recovery_rate = a[5]
        r_county_pop = a[6]
        r_county_pop_density = a[7]
        r_prob_visiting_grocery_store = a[8]
        r_prob_visiting_restaurant = a[9]
        r_prob_visiting_park = a[10]
        infection_margin = a[11]
        mortality_margin = a[12]
        recovery_margin = a[13]
        print(county_list[curr_county], timeperiod_1[time_index], timeperiod_2[time_index])
        # parameter estimation
        w = np.arange(0.05, 0.65, 0.05)  # ratio of susceptible to total population
        alpha = np.arange(0.05, 0.55, 0.05).round(2)  # asymptomatic rate e.g. 0.16
        # beta = np.arange(0.05,1,0.05)  # infection rate
        # gamma = np.arange(0.05,1,0.05) # recovery rate
        # ups = np.arange(0.05,1,0.05)  # mortality rate

        P = r_county_pop
        Theta = len(r_confirmed_cases)  # time windows
        S, I, R, D = [0]*Theta, [0]*Theta, [0]*Theta, [0]*Theta

        rho = 0.9  # exponential decay weight
        # params = np.array([beta, gamma, ups])
        # dt = np.dot(Phi,params)

        AW = []
        Phi = {}
        dt_mx = np.zeros((len(alpha), Theta-1, 3))

        for i in range(len(w)):
            for j in range(len(alpha)):
                for day in range(Theta):
                    D[day] = r_confirmed_deaths[day]
                    R[day] = alpha[j]*r_confirmed_recoveries[day]
                    I[day] = alpha[j]*r_confirmed_cases[day]
                    S[day] = w[i]*alpha[j]*P - I[day] - R[day] - D[day]
                    AW.append([w[i], alpha[j], S[day], I[day], R[day], D[day]])
                    phi = calculate_Phi(S[day], I[day], alpha[j])
                    phi = np.multiply(rho**(Theta - day), phi)
                    Phi.update({(w[i], alpha[j], day): phi})
                for day in range(1, Theta-1):
                    dt_mx[j][day][0] = alpha[j]*r_confirmed_cases[day] - alpha[j]*r_confirmed_cases[day-1]
                    dt_mx[j][day][1] = alpha[j]*r_confirmed_recoveries[day] - alpha[j]*r_confirmed_recoveries[day-1]
                    dt_mx[j][day][2] = r_confirmed_deaths[day] - r_confirmed_deaths[day-1]
                    dt_mx[j][day] = np.multiply(rho**(Theta - day), dt_mx[j][day])
        '''
        # Sample Test
        sample_phi = Phi.get((0.05, 0.05, 0))
        for i in range(1, len(r_confirmed_cases)-1):
            next_phi = Phi.get((0.45, 0.15, i))
            sample_phi = np.concatenate((sample_phi, next_phi))

        Phi_pinv = la.pinv(sample_phi)
        sample_dt_mx = np.hstack(dt_mx[0])
        # print(Phi_pinv.shape, sample_dt_mx.shape)
        
        params = np.dot(Phi_pinv, sample_dt_mx)
        '''
        params = {}
        mseList = {}
        for i in w:
            for j in range(len(alpha)):
                phi = Phi.get((i, alpha[j], 0))
                for m in range(1, Theta-1):
                    next_phi = Phi.get((i, alpha[j], m))
                    phi = np.concatenate((phi, next_phi))
                Phi_pinv = la.pinv(phi)
                dt = np.hstack(dt_mx[j])
                param = np.dot(Phi_pinv, dt)
                params.update({(i, alpha[j]): param})
                mse = loss_function(dt, phi, param)
                mseList.update({(i, alpha[j]): mse})
                
        result = min(mseList, key = mseList.get)
        final_params = params.get(result)
        #final_params = mseList.get(result)[0]
        # w, alpha, beta, gamma, ups = [0.05, 0.05, 0.01814779, 0.00398241, 0.00184115]
        final_copy_row.append([county_list[curr_county], timeperiod_1[time_index], timeperiod_2[time_index], result, final_params])
        print(result)
        print(final_params)

# Writing the final values to a CSV file
filename = "output.csv"
fields = ['County', 'Start date', 'End date', 'w, alpha', 'beta, gamma, ups']
# writing to csv file
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(final_copy_row)
