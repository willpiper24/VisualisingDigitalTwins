import csv
import numpy as np
import json
import subprocess

with open("All_the_data.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    x = list(csv_reader)
    data = np.array(x)
csv_file.close()

data_dict = {}
data_dict['michael_data'] = {}
for column in range(0, len(data[0][:])):
    time = str(data[1][column])
    data_dict['michael_data'][time] = {}
    data_dict['michael_data'][time]['carbon_emission'] = str(data[0][column])
    data_dict['michael_data'][time]['time'] = str(data[1][column])
    data_dict['michael_data'][time]['electricity_to_use'] = str(data[2][column])
    data_dict['michael_data'][time]['electricity_generated'] = str(data[3][column])
    data_dict['michael_data'][time]['battery_soc'] = str(data[4][column])
    data_dict['michael_data'][time]['electricity_price'] = str(data[5][column])
    data_dict['michael_data'][time]['electricity_to_buy'] = str(data[6][column])
    data_dict['michael_data'][time]['LED_mode'] = str(data[7][column])
    data_dict['michael_data'][time]['hourly_traffic'] = str(data[8][column])
    data_dict['michael_data'][time]['PV'] = str(data[9][column])

with open("All_the_data.json", 'w') as outfile:
    json.dump(data_dict, outfile)
subprocess.run(['scp', 'All_the_data.json', 'pi@192.168.1.246:/home/pi/Documents/dtserver/All_the_data.json'])