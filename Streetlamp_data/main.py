import csv
import numpy as np
import json
import subprocess
import os
import time

def run():
    if os.path.exists('All_the_data.csv'):
        os.remove('All_the_data.csv')
    subprocess.run(['matlab', '-batch', 'Virtual_Test'])

    with open("All_the_data.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        x = list(csv_reader)
        data = np.array(x)
    csv_file.close()

    csv_path = os.path.join('..','LSTM','15_steps_in_34943_sample_predicted.csv')
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        LSTM_data = list(csv_reader)[0]
        LSTM_data = [float(i) for i in LSTM_data]
    csv_file.close()

    data_dict = {}
    data_dict['michael_data'] = {}
    data_dict['LSTM_data'] = {}
    for column in range(48):
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
        #data_dict['michael_data'][time]['PV'] = str(data[9][column])
        data_dict['LSTM_data'][time]['predicted_traffic'] = str(round(sum(LSTM_data[int(float(time)/0.25):int(float(time)/0.25+2)])))

    with open("All_the_data.json", 'w') as outfile:
        json.dump(data_dict, outfile)

    subprocess.run(['scp', 'All_the_data.json', 'pi@192.168.1.246:/home/pi/Documents/dtserver/All_the_data.json'])

while True:
    run()
    time.sleep(5)
