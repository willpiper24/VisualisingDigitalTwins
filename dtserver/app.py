from flask import Flask, render_template, jsonify, request, send_file
import json
import time
from numpy import random
import time
import board
import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn
from adafruit_pcf8591.analog_out import AnalogOut

app = Flask(__name__)

i2c = board.I2C()
pcf = PCF.PCF8591(i2c)
pcf_in_0 = AnalogIn(pcf, PCF.A0)
pcf_out = AnalogOut(pcf, PCF.OUT)

@app.route("/api")
def home():
#     read brightness
    set_brightness = float(request.args.get('brightness'))

#     set voltage
    max_voltage = 3.3
    set_voltage = (set_brightness*max_voltage)/100
    
#     read voltage
    pcf_out.value = round(float(65535)*(set_voltage/max_voltage))
    raw_value = pcf_in_0.value
    read_voltage = round((raw_value/65535)*pcf_in_0.reference_voltage,3)
    
#     create JSON file containing voltage, current and brightness
    resistance = 330
    current = round(read_voltage/resistance,6)
    data_dict = {}
    data_dict['real_data'] = {}
    data_dict['real_data']['brightness'] = str(set_brightness)
    data_dict['real_data']['current'] = str(current)
    data_dict['real_data']['voltage'] = str(read_voltage)
    
    with open("All_the_data.json") as json_file:
        json_data = json.load(json_file)
        
    output_data = data_dict | json_data
    
    return jsonify(**output_data)

@app.route('/get_image')
def get_image():
    return send_file('net_power_demand.png')
