import csv
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
    csv_file.close()

    LSTM_csv_path = os.path.join(LSTM_dir,'LSTM_data.csv')
    with open(LSTM_csv_path) as csv_file:
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
        #data_dict['LSTM_data'][time]['predicted_traffic'] = str(round(sum(LSTM_data[int(float(time)/0.25):int(float(time)/0.25+2)])))
        data_dict['LSTM_data'][time]['predicted_traffic'] = str(round(sum(LSTM_data[column*2:column*2+2])))

    with open('All_the_data.json', 'w') as outfile:
        json.dump(data_dict, outfile)

    subprocess.run(['scp', 'All_the_data.json', 'pi@192.168.1.246:/home/pi/Documents/dtserver/All_the_data.json'])

while True:
    run()
    time.sleep(5)

run()
