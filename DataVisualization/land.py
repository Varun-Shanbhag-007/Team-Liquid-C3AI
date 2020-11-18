import pandas as pd

county_rec_excel = pd.ExcelFile('/data/county_land_area.xlsx')
county_rec_df = pd.read_excel(county_rec_excel, 'county_land_area', header = 0)

county_rec_df['State'] = county_rec_df['Areaname'].apply(lambda x: x.split(','))
county_rec_df = county_rec_df[county_rec_df['State'].apply(lambda x: len(x)) > 1]
county_rec_df = county_rec_df.reset_index(drop=True)

state = pd.read_csv('/data/state_code.csv', header = 0)

for y in range(len(state['Code'])):
    for x in range(len(county_rec_df['Areaname'])):
        if county_rec_df['Areaname'][x][-2:] == state['Code'][y]:
            county_rec_df['Areaname'][x] = county_rec_df['Areaname'][x].replace(county_rec_df['Areaname'][x][-2:], state['State'][y])

county_rec_df['Areaname'] = county_rec_df['Areaname'].apply(lambda x: x.replace(', ','_')+'_UnitedStates')

county_rec_df = county_rec_df.drop(columns=['State'])

county_rec_df.to_csv('/data/county_land_area_formatted.csv', index=False)
