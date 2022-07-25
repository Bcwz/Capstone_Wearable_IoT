import os
import random
import time
import subprocess
import atexit
import requests
import csv

from dotenv import load_dotenv
from datetime import datetime
from Thingsboard.connection import Thingsboard
from Sensors.DHT11.dht11 import DHT11
from Calculation.wet_bulb_globe_temperature import WBGT
from Connectivity.connectivity import CONNECTIVITY
#from Database.mongodb import mongoDatabase


load_dotenv()
MONGODB_URL = os.getenv('MONGODB_BASEURL')
POLLING_RATE_SECONDS = 120
data_pin = 24
TURN_OFF_USB = './uhubctl/turnoff.sh'
#SERVER_IP = '172.20.10.6'
SERVER_IP = '192.168.86.29'
SERVER_PORT = 5000
#SERVER_FORECAST_ENDPOINT = 'http://172.20.10.6:5000/forecast'
#SENSOR_DATA_ENDPOINT = 'http://172.20.10.6:5000/sensor_data'
SERVER_FORECAST_ENDPOINT = 'http://192.168.86.29:5000/forecast'
SENSOR_DATA_ENDPOINT = 'http://192.168.86.29:5000/sensor_data'

def main():
    while True:
        DHT = DHT11(data_pin)
        #Poll temperature and humidity from DHT11 sensors and pass to WBGT to calculate.
        try:
            temperature,humidity = DHT.temp_hum()
           
                        
            status = CONNECTIVITY.check_connectivity(SERVER_IP,SERVER_PORT)
            
            if(status == True):
                print("INTERNET TRUE")
                wbgt = WBGT.calculate(temperature,humidity)
                wbgt_float = float("{:.2f}".format(wbgt))
                sensor_data = requests.post(SENSOR_DATA_ENDPOINT, json={'sensor_wbgt':wbgt_float})
                forecast_wbgt = requests.get(SERVER_FORECAST_ENDPOINT)
                print(forecast_wbgt.json()["forecast_wbgt"])
                forecast_wbgt_float = float(forecast_wbgt.json()["forecast_wbgt"])
                WBGT.risk_level(forecast_wbgt_float)                
            else:
                #Pass in temp & humidity to calculate Wet-Bulb Globe Temperature, using WBGT = 0.7 * Tw + 0.3 * T
                print("INTERNET FALSE")  
                wbgt = WBGT.calculate(temperature,humidity)
                wbgt_float = float("{:.2f}".format(wbgt))
                WBGT.risk_level(wbgt_float)
                             
            
            time.sleep(POLLING_RATE_SECONDS)
        except Exception as e:
            print(e)
            continue


def exit_program():
    subprocess.call(TURN_OFF_USB)
    print("EXITING PROGRAM")

if __name__ == "__main__":
    subprocess.call(TURN_OFF_USB,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    main()
    