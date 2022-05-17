import time
import Adafruit_DHT

class DHT11:
    def __init__(self,GPIO_pin):
        """Class method for DHT11, takes in GPIO_pin argument"""
        # Sensor should be set to Adafruit_DHT.DHT11,
        # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
        self.sensor = Adafruit_DHT.DHT11
        self.GPIO_pin = GPIO_pin
        
    def temp_hum(self):
        """Method to return temperature(*C) and humidity (%), takes in one integer/float argument for polling rate in seconds"""
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.GPIO_pin)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            return (temperature,humidity)
        else:
            print('Failed to get reading. Try again!')
            
            
    def temp(self,polling_rate_seconds):
        """Method to return temperature(*C), takes in one integer/float argument for polling rate in seconds"""
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.GPIO_pin)
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C'.format(temperature))
                return (temperature)
            else:
                print('Failed to get reading. Try again!')
            time.sleep(polling_rate_seconds)
        
    def humidity(self,polling_rate_seconds):
        """Method to return humidity (%), takes in one integer/float argument for polling rate in seconds"""
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.GPIO_pin)
            if humidity is not None and temperature is not None:
                print('Humidity={0:0.1f}%'.format(humidity))
                return (humidity)
            else:
                print('Failed to get reading. Try again!')
            time.sleep(polling_rate_seconds)
            
            
    
#test = DHT11(24)
#test.humidity(1)