import os
import random
import time
import subprocess
import atexit

from dotenv import load_dotenv
from datetime import datetime
from Thingsboard.connection import Thingsboard
from Sensors.DHT11.dht11 import DHT11
from Calculation.wet_bulb_globe_temperature import WBGT
from Connectivity.connectivity import CONNECTIVITY
#from Database.mongodb import mongoDatabase


load_dotenv()
MONGODB_URL = os.getenv('MONGODB_BASEURL')
POLLING_RATE_SECONDS = 2
data_pin = 24
GOOGLE_IP = '8.8.8.8'
TURN_OFF_USB = './uhubctl/turnoff.sh'


def main():
    while True:
        DHT = DHT11(data_pin)
        #Poll temperature and humidity from DHT11 sensors and pass to WBGT to calculate.
        try:
            temperature,humidity = DHT.temp_hum()
           
                        
            status = CONNECTIVITY.check_connectivity(GOOGLE_IP)
            
            if(status == True):
                #TODO Pass in WBGT to ML model to detect and predict if wearer is at risk of heat injuries.
                #Send Temp, humidity, wbgt to Thingsboard
                #Thingsboard.post(humidity,temperature, wbgt)
                wbgt = WBGT.calculate(temperature,humidity)
                WBGT.risk_level(wbgt)
                #print("INTERNET TRUE= " + str(wbgt))  
                pass
            else:
                #Pass in temp & humidity to calculate Wet-Bulb Globe Temperature, using WBGT = 0.7 * Tw + 0.3 * T
                wbgt = WBGT.calculate(temperature,humidity)
                WBGT.risk_level(wbgt)
                #print("INTERNET FALSE = " + str(wbgt))               
            
            time.sleep(POLLING_RATE_SECONDS)
        except:
            continue

def exit_program():
    subprocess.call(TURN_OFF_USB)
    print("EXITING PROGRAM")

if __name__ == "__main__":
    subprocess.call(TURN_OFF_USB,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    main()
    