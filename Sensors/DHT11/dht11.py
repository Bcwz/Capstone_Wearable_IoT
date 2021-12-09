import time
import Adafruit_DHT


class DHT11:
    def __init__(self,GPIO_pin):
        # Sensor should be set to Adafruit_DHT.DHT11,
        # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
        self.sensor = Adafruit_DHT.DHT11
        self.GPIO_pin = GPIO_pin
        
    def temp_hum(self,polling_rate):
        """Method to return temperature(*C) and humidity (%), takes in one integer/float argurment for polling rate in seconds"""
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.GPIO_pin)
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            else:
                print('Failed to get reading. Try again!')
            time.sleep(polling_rate)
            
    def temp(self,polling_rate):
        """Method to return temperature(*C), takes in one integer/float argurment for polling rate in seconds"""
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.GPIO_pin)
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C'.format(temperature))
            else:
                print('Failed to get reading. Try again!')
            time.sleep(polling_rate)
        
    def humidity(self,polling_rate):
        """Method to return humidity (%), takes in one integer/float argurment for polling rate in seconds"""
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.GPIO_pin)
            if humidity is not None and temperature is not None:
                print('Humidity={0:0.1f}%'.format(humidity))
            else:
                print('Failed to get reading. Try again!')
            time.sleep(polling_rate)
            
    
#test = DHT11(24)
#test.humidity(1)