## Description
### get_simulation_data - 
Given a county along with the start and the end date for simulation, this function returns the data required for simulation.  
The number of confirmed cases, deaths, and recoveries for a given county are retrieved from the data provided by Johns Hopkins University and Corona Data Scraper through the OutbreakLocation API. Using this data infection_rate, mortality_rate and recovery_rate are calculated.  
Furthermore, the population of the given county is retrieved from the data provided by US Census Bureau through the PopulationData API.  
To calculate probabilities of a person visiting a grocery store, a restaurant, and a visiting park are calculated using mobility data provided by Google through OutbreakLocation API along with three external sources [1, 2, 3]. These external sources provide probabilities of an American person going to a grocery store, a restaurant, and a visiting park.  
Google's mobility data provides normalized trends for the given range of dates. 

### plot_SIR_graph - 
Given a county, start and end date for the SIR graph along with the w value, this function plots the SIR graph for it.  
The w value is a fraction of the population that is the initial susceptible population.  
The number of confirmed cases, deaths, and recoveries for a given county are retrieved from the data provided by Corona Data Scraper through the OutbreakLocation API.  
The population of the given county is retrieved from the data provided by US Census Bureau through the PopulationData API. 

## Examples
### get_simulation_data - 
confirmed_cases, confirmed_deaths, confirmed_recoveries, infection_rate, mortality_rate,recovery_rate, county_pop, prob_visiting_grocery_store, prob_visiting_restaurant, prob_visiting_park = preparedata.get_simulation_data('Kern_California_UnitedStates','2020-05-01','2020-08-29')

### plot_SIR_graph - 
preparedata.plot_SIR_graph(county = "Harris_Texas_UnitedStates", start_date = "2020-03-01", end_date = "2020-10-01", w = 0.1)


## Sources
### From C3.ai COVID-19 Data Lake
DEMOGRAPHICS - PopulationData  
DAILY CASE REPORTS & MOBILITY - OutbreakLocation

### External Sources
Probability an American person goes to a grocery store  
[1] https://spendmenot.com/blog/grocery-shopping-statistics/#:~:text=Grocery%20stores%20in%20the%20US,million%20from%20Friday%20to%20Sunday.  

Probability an American person goes to a park  
[2] https://www.smallbizgenius.net/by-the-numbers/restaurant-industry-statistics/#gref  

    
Probability an American person goes to a restaurants  
[3] https://www.nrpa.org/blog/29-number-of-times-americans-visit-their-local-parks-annually/ https://www.nps.gov/aboutus/visitation-numbers.htm
