import numpy
import subprocess

from fractions import Fraction
from datetime import datetime


WBGT_THRESHOLD = 27.0
TURN_ON_USB = './uhubctl/turnon.sh'
TURN_OFF_USB = './uhubctl/turnoff.sh'

risk_high_black = 29.0
risk_high_red = 28.0
risk_medium_yellow = 27.0
risk_low_green = 26.0 
risk_low_white = 25.9 

class WBGT:    
    def calculate(temperature, humidity):
        # Tw = wet-bulb temperature
        # T = current temperature
        # rh% = current humidity
        # Tw = T * arctan[0.151977 * (rh% + 8.313659)^(1/2)] + arctan(T + rh%) - arctan(rh% - 1.676331) + 0.00391838 *(rh%)^(3/2) * arctan(0.023101 * rh%) - 4.686035
        tw = temperature * numpy.arctan(0.151977 * pow((humidity + 8.313659),(1/2))) + numpy.arctan(temperature + humidity) - numpy.arctan(humidity - 1.676331 )  + 0.00391838 * (pow(humidity,Fraction(3,2))) * numpy.arctan(0.023101 * humidity) - 4.686035
        # print("tw = " + str(tw))        

        # WBGT = 0.7 * Tw + 0.3 * T
        wbgt = 0.7 * tw + 0.3 * temperature
        print("WBGT = " + str(wbgt))
        
        return wbgt
    
    def risk_level(wbgt):
        now = datetime.now()
        if(wbgt>=float(risk_high_red)):            
            print("HIGH RISK ALERT", now,"\n")
            subprocess.call(TURN_ON_USB,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif (wbgt>=float(risk_medium_yellow) and wbgt <float(risk_high_red)):
            print("MEDIUM RISK ALERT",now,"\n")
            subprocess.call(TURN_ON_USB,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print("LOW RISK ALERT",now,"\n")
            subprocess.call(TURN_OFF_USB,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
