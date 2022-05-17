import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

THINGSBOARD_URL = os.getenv('THINGSBOARD_URL')
ACCESS_TOKEN = os.getenv('THINGSBOARD_ACCESS_TOKEN')

sensor_data = {'temperature': 0, 'humidity': 0, 'wbgt':0, 'date': 0,'time': 0, 'longitude': 0,'latitude': 0}
LONGITUDE = 103.849199  #longitude for NYP, hardcoded
LATITUDE = 1.377262 # latitude for NYP, hardcoded



class Thingsboard:

    def post(humidity,temperature, wbgt ):
        client = mqtt.Client()
        client.username_pw_set(ACCESS_TOKEN)
        client.connect(THINGSBOARD_URL, 1883, 60)
        client.loop_start()
        #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        now = datetime.now()
        date_now = now.strftime("%d/%m/%Y")
        time_now = now.strftime("%H:%M:%S")
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity
        sensor_data['wbgt'] = wbgt
        sensor_data['date'] = date_now
        sensor_data['time'] = time_now
        sensor_data['longitude'] = LONGITUDE
        sensor_data['latitude'] = LATITUDE                
        # Sending humidity, temperature, date & time data to ThingsBoard using MQTT QoS 2
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 2)
        client.loop_stop()
        #client.disconnect()

            