## Model
This folder consists of python files that retrieve the data from c3aidatalake, preprares it and calculates w, alpha and beta parameters needed for the simulation. <br/>
The file param.py consists of all the caluclations needed to be done. It gets the county data and time period from calc_delta.py and returns a csv file with counties, time periods and the required parameters during those time periods.
