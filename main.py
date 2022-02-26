import csv
from dataclasses import dataclass
from matplotlib.cbook import maxdict
import numpy as np
import json
import subprocess
import os
import time

def run():
    streetlightdata_dir = os.path.join(os.getcwd(),'StreetlightData')
    LSTM_dir = os.path.join(os.getcwd(),'LSTM')
    if os.path.exists(os.path.join(streetlightdata_dir,'All_the_data.csv')):
        os.remove(os.path.join(streetlightdata_dir,'All_the_data.csv'))
    subprocess.run(['matlab', '-batch', 'Virtual_Test'], cwd=streetlightdata_dir)
    subprocess.run(['python', 'multi-step_traffic_LSTM.py'], cwd=LSTM_dir)

    streetlightdata_csv_path = os.path.join(streetlightdata_dir,'All_the_data.csv')
    with open(streetlightdata_csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        x = list(csv_reader)
        data = np.array(x)
        max_PV = float(max(data[8]))
    csv_file.close()

    LSTM_csv_path = os.path.join(LSTM_dir,'LSTM_data.csv')
    with open(LSTM_csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        LSTM_data = list(csv_reader)[0]
        LSTM_data = [float(i) for i in LSTM_data]
    csv_file.close()

    max_traffic_list = []
    for i in range(len(LSTM_data)-1):
        max_traffic_list.append(LSTM_data[i]+LSTM_data[i+1]) 
        max_traffic = max(max_traffic_list)

    data_dict = {}
    data_dict['michael_data'] = {}
    data_dict['LSTM_data'] = {}
    for column in range(24):
        time = str(data[1][column])
        data_dict['michael_data'][time] = {}
        data_dict['LSTM_data'][time] = {}
        data_dict['michael_data'][time]['carbon_emission'] = str(data[0][column])
        data_dict['michael_data'][time]['time'] = str(data[1][column])
        data_dict['michael_data'][time]['electricity_to_use'] = str(data[2][column])
        data_dict['michael_data'][time]['electricity_generated'] = str(data[3][column])
        data_dict['michael_data'][time]['battery_soc'] = str(data[4][column])
        data_dict['michael_data'][time]['electricity_price'] = str(data[5][column])
        data_dict['michael_data'][time]['electricity_to_buy'] = str(data[6][column])
        data_dict['michael_data'][time]['LED_mode'] = str(data[7][column])
        #data_dict['michael_data'][time]['hourly_traffic'] = str(data[8][column])
        predicted_PV = float(data[8][column])
        data_dict['michael_data'][time]['predicted_PV'] = str(predicted_PV)
        #data_dict['LSTM_data'][time]['predicted_traffic'] = str(round(sum(LSTM_data[int(float(time)/0.25):int(float(time)/0.25+2)])))
        predicted_traffic = sum(LSTM_data[column*2:column*2+2])
        data_dict['LSTM_data'][time]['predicted_traffic'] = str(round(predicted_traffic))
        base_brightness = 50
        data_dict['LSTM_data'][time]['predicted_brightness'] = str(round(base_brightness + (predicted_traffic/max_traffic)*(1-predicted_PV/max_PV)*(100-base_brightness),1))

    with open('All_the_data.json', 'w') as outfile:
        json.dump(data_dict, outfile)

    subprocess.run(['scp', 'All_the_data.json', 'pi@192.168.1.246:/home/pi/Documents/dtserver/All_the_data.json'])
    subprocess.run(['scp', os.path.join(streetlightdata_dir,'net_power_demand.png'), 'pi@192.168.1.246:/home/pi/Documents/dtserver/net_power_demand.png'])

#while True:
    #run()
    #time.sleep(5)

run()
