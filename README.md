## Project Structure :
---
### Project is divided into 3 folders:

- Animation folder consist code for simulation 
- Data Visulization scrapes data used for training model
Model
- Model Folder consist of model which provides animation module with required values to run simulation
- Result Folder holds simulation result and over all impact using solution


### Team Liquid Report : Anonymous Contact Tracing and Mitigating Spread of COVID-19 using Bluetooth Device

### Introduction
---
In order to effectively mitigate the spread of COVID-19, this paper suggests an anonymous contact tracing and visualization system to track the infected population, record a probable infected score, and a heat map that provides insights on how risky a certain location is to travel to. A Susceptible-Infected-Recovered model simulation is conducted to mathematically prove the effectiveness of the system. The rate of spread, contraction radius, mobility factors (probability of going to grocery stores, restaurants, parks) are data-driven numbers and are considered in estimating the parameters in the SIR model and for conducting the simulation of our solution.
 
### Problem Description
---
Considering the intervention policies implemented in many countries might not be effective to mitigate the spread of COVID-19, this study proposes a system to mitigate the spread of the disease by reducing social interactions. Given a real-time heat map, the public could understand the risk of travelling to a certain location based on the population already there, without revealing any identities. Each user is assigned a COVID_score based on their exposure to infected individuals which is tracked by our device. The individual’s score is only accessible to themselves, but the heat map will reflect the location risk anonymously as it only shows an aggregated number. When such a system is followed, our model shows that the number of cases could be reduced by ~33%.

### Broad Approach
---
Considering the willingness of people to participate, each device is linked to a central secure server that has access to all COVID tests. It keeps track of all the people who test positive. The system separately also assigns COVID_scores based on the possibility of having contracted the disease for people who are not definitively tested based on their interactions with those that are positive.
 
The system is only to inform the public. Regardless of the information we provide, the decision to travel is their own and we do not enforce any regulations. We have taken this into account while building our model. In addition, this may also be beneficial to public places (malls, shops, restaurants, etc.) that choose to have their spaces open and want to guarantee safety. They can use our COVID_score to limit the entry of asymptomatic individuals or other high risk score individuals (Replace the current system of simply scanning the temperature at entry with this).
 
The heart of the project comes from looking at the SIR model and trying to build a system / solution that can help make a “better” curve in case of a similar pandemic in the future. A better curve is one in which the Infected line in the SIR model has the least area under it.

### Technical Details of Approach
---
The parameter estimation for the SIR model followed an algorithm suggested by Calafiore, Novara, and Possieri (2020), which simulated a modified SIR model for Italy cities. Focusing on some U.S. counties, necessarily with complete data of the infected, the recovered, and deaths, and preferably with higher population, the data between March and August from C3.AI data lake was fetched and modelled under different time intervals and windows. The parameters of infection rate, asymptomatic rate, susceptible rate, recover rate, and mortality rate were estimated using an iterative mean squared error algorithm. The final parameter values are the mean of the estimated results.
 
In simulating the random model, the same parameters were used, however, they were scaled down so that it can be simulated on a computer. We show that the curve from the SIR model is similar to the curve that our simulation generates in normal conditions in an average social distancing norm, as proof that the simulation can approximately replicate the results of real-world conditions. 
 
Next, we implemented our solution where, when a person decides on a certain location to travel to, we show the risk of contracting the disease in that travel based on the susceptible and infected population that are already present in that place. This should help the user make a decision on whether they want to make the trip or not. In our simulation, we have chosen to base this on 3 locations that people visit (grocery store, restaurant, park) and their home. The probability of a person going to those places is based on data that we were able to gather from the C3.AI datalake sources.
 
We have estimated that the radius of spread and the probability of COVID spread comes from data. So when a susceptible person is within the spread-radius of an infected person, there is a probability that the susceptible person contracts the disease. Thus the infection is spread. We also implement a forced self-quarantine after 2 days of infection, thus that person is unable to spread the disease. Based on our passage of time in the simulation, an infected person is cured after 14 simulation days. 
 
Using these data points, we plot our own SIR curve with values updating each iteration to come up with the solution plot.

### Results
---
In the SIR model, Kern County in California is our target. Despite a dynamic change of parameter values under different time windows, the average infection rate is 0.064 given the susceptible population as 5% of the total population in Kern with 15% of infected people being asymptomatic. 
 
Implementing our solution, we were able to simulate using the same values as above,  and found that the total infection reduced by ~33% and the spread of the infection was quickly and effectively reduced. Note that the simulation takes into account the fact that people are not always compliant.
 
### Impact
---
With this solution, we propose a policy / method of dealing with the virus where everyone is equally aware of the situation in real-time. This incentivizes people to work together to fight a pandemic of this type so that the disease can be eradicated quicker and normal conditions can be re-established from a socio-economic perspective.
 
We want this to be a viable option in case of a future pandemic that we may have to deal with, or even for fighting COVID-19 in case a vaccine is not available in the near future.
