import pandas as pd
import numpy as np
import c3aidatalake

def get_simulation_data(county, start_date, end_date):
    population = c3aidatalake.fetch(
        "populationdata",
        {
            "spec": {
                "filter": "contains(parent, '"+county+ "') && (populationAge == '<18' || populationAge == '18-64' || populationAge == '>=65' || populationAge == 'Total') && gender == 'Male/Female' && year == 2018",
                "limit": -1
              }
        },
        get_all = True
    )

    county_total_pop = int((population['value'].loc[population['populationAge'] == 'Total']).values[0])

    today = pd.Timestamp.now().strftime("%Y-%m-%d")

    casecounts = c3aidatalake.evalmetrics(
        "outbreaklocation",
        {
            "spec" : {
                "ids" : [county],
                "expressions" : ["JHU_ConfirmedCases", "JHU_ConfirmedDeaths", "CDS_Recovered"],
                "start" : start_date,
                "end" : end_date,
                "interval" : "DAY",
            }
        }
    )
    casecounts = casecounts.loc[:,~casecounts.columns.str.contains('^dates', case=False)] 
    casecounts = casecounts[casecounts.columns.drop(list(casecounts.filter(regex='.missing')))]
    confirmed_cases = [int(casecounts.iloc[i,0]) for i in range(len(casecounts))]
    confirmed_recoveries = [int(casecounts.iloc[i,1]) for i in range(len(casecounts))]
    confirmed_deaths = [int(casecounts.iloc[i,2]) for i in range(len(casecounts))]
    infection_rate = [round((infected /county_total_pop),4) for infected in confirmed_cases]  #beta
    recovery_rate = [round((confirmed_recoveries[j]/ confirmed_cases[j]),4)  for j in range(len(confirmed_recoveries))]
    mortality_rate = [round((confirmed_deaths[j]/ confirmed_cases[j]),4)  for j in range(len(confirmed_deaths))]
    
    area_df = pd.read_csv('counties_area.csv')
    county_area = area_df['Area'].loc[area_df['County']==county].values[0]
    county_pop_density = round((county_total_pop/ county_area),2)

    us_percent_people_visit_grocery_everyday = round((31*100/328),2)
    us_percent_people_visiting_restaurant = round((170*100/328),2)
    us_percent_people_going_to_parks = round((30*100/365),2)

    mobility_trends = c3aidatalake.evalmetrics(
        "outbreaklocation",
        {
            "spec" : {
                "ids" : [county],
                "expressions" : [
                    "Google_ParksMobility",
                    "Google_GroceryMobility",
                    "Google_RetailMobility",
                    "Google_ResidentialMobility"

                  ],
                "start" : start_date,
                "end" : end_date,
                "interval" : "DAY",
            }
        },
        get_all = True
    )

    prob_visiting_grocery_store = (mobility_trends[county+".Google_GroceryMobility.data"].values * (us_percent_people_visit_grocery_everyday/100))/100
    prob_visiting_restaurant = (mobility_trends[county+".Google_RetailMobility.data"].values * (us_percent_people_visiting_restaurant/100))/100
    prob_visiting_park = (mobility_trends[county+".Google_ParksMobility.data"].values * (us_percent_people_going_to_parks/100))/100

    return confirmed_cases, confirmed_deaths, confirmed_recoveries, infection_rate, mortality_rate, recovery_rate, county_total_pop, county_pop_density, prob_visiting_grocery_store, prob_visiting_restaurant, prob_visiting_park