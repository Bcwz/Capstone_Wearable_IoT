import os
import random
from dotenv import load_dotenv
from datetime import datetime
import time
#from Sensors.DHT11.dht11 import DHT11
from Calculation.wet_bulb_globe_temperature import WBGT
from Database.mongodb import mongoDatabase

load_dotenv()
MONGODB_URL = os.getenv('MONGODB_BASEURL')
POLLING_RATE_SECONDS = 5

def main():
    while True:
        #Poll temperature and humidity from DHT11 sensors and pass to WBGT to calculate.
        temp = random.randrange(20.00, 30.00)
        humidity = random.randrange(60.00, 100.00)
        #temperature,humidity = DHT11.temp_hum(POLLING_RATE_SECONDS)
        #Pass in temp & humidity to calculate Wet-Bulb Globe Temperature, using WBGT = 0.7 * Tw + 0.3 * T
        wbgt = WBGT.calculate(temp,humidity)
        # print(wbgt)
        #TODO Pass in WBGT to ML model to detect and predict if wearer is at risk of heat injuries.
        time.sleep(POLLING_RATE_SECONDS)
        
       


if __name__ == "__main__":
    main()