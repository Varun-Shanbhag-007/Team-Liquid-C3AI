import os
import pandas as pd
import datetime

path = os.path.dirname(__file__)
countypath = path+'/data/County_w_Recovered.csv'

# This function returns a list of the counties with the format "Countyname_State_UnitedStates" from the list of
# counties that have recovered data, taken from Counties_w_Recovered.csv
def get_county_list():
    df = pd.read_csv(countypath).fillna('')
    currstate = ""
    full_county_names = []
    for i in range(len(df)):
        if df["state"][i] != "":
            currstate = df["state"][i]
        else:
            df["state"][i] = currstate
        format_county_name = df["county"][i].replace(" ", "")
        if format_county_name != "":
            county_pre_name = format_county_name.replace("County", "")
        # county_name_len = len(df["county"][i].replace(" ", "")) - 6
        # county_pre_name = df["county"][i][0:county_name_len]
            full_county_names.append(county_pre_name+"_"+currstate+"_UnitedStates")
    return full_county_names


# This function returns 2 lists, one with the start data and the other with the end date of the time periods that are
# being considered for the parameter calculation. As of now, the dates start from 2020-03-02 to 2020-09-28 with the
# time period of 2 weeks. This can be adjusted as needed.
def get_time_period():
    aDate1 = datetime.datetime.strptime("2020-05-01", "%Y-%m-%d") # Start date of the first time period
    aDate2 = datetime.datetime.strptime("2020-05-15", "%Y-%m-%d") # End date of the first time period
    time_period = datetime.timedelta(weeks=2)                     # Time period being considered, eg. 2 weeks
    final_dates1 = [str(aDate1)[0:10]]                            # Extracts the date from the datetime object
    final_dates2 = [str(aDate2)[0:10]]
    for i in range(7):
        aDate1 = aDate1 + time_period
        aDate1_str = str(aDate1)
        final_dates1.append(aDate1_str[0:10])
        aDate2 = aDate2 + time_period
        aDate2_str = str(aDate2)
        final_dates2.append(aDate2_str[0:10])
    return final_dates1, final_dates2
