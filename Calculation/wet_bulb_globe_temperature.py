from fractions import Fraction
import numpy


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
        #print("WBGT = " + str(wbgt))
        return wbgt
        
