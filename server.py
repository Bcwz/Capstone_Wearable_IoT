import pandas as pd
import json
import numpy as np
import math
from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, request,jsonify

 

app = Flask(__name__)
df = pd.read_csv('.\Machine_Learning\Dataset\server_two-hundred-fourty-second-wbgt.csv')
current_array = df.to_numpy()

NUMBER_OF_DAYS =0.5
NUMBER_OF_DATA_POINT =  math.floor((NUMBER_OF_DAYS * 86400)/240)

NUMBER_OF_FORECAST_STEPS = 5

current_array = current_array[len(current_array) - NUMBER_OF_DATA_POINT - 1:]
train_size = math.floor(0.8*NUMBER_OF_DATA_POINT)
test_size =math.floor(NUMBER_OF_DATA_POINT)


@app.route("/", methods=['GET'])
def hello():
    return 'Hello World!'

@app.route("/forecast", methods=['GET'])
def return_forecast_data():
    arima_value = arima()
    return jsonify({'forecast_wbgt' : arima_value.json})

@app.route("/ip", methods=['GET'])
def my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.route("/csv_data", methods=['GET'])
def csv_data():
    print(len(current_array))
    return f'{current_array}'

@app.route("/sensor_data", methods=['POST'])
def sensor_data():
    global current_array
    data = request.json
    print(data["sensor_wbgt"])
    sensor_data = data["sensor_wbgt"]
    update_array = current_array[1:]
    update_array = np.append(update_array,float(sensor_data))
    current_array = update_array
    # df_array = df_array.append(data["sensor_wbgt"])
    #return jsonify(data)
    return f'{current_array}'

def arima():
    train = current_array[0:train_size]
    #test = current_array[train_size:test_size]
    model = ARIMA(train, order=(1,1,5))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=NUMBER_OF_FORECAST_STEPS)
    max_forecast = max(forecast)
    max_forecast_2deci = float("{:.2f}".format(max_forecast))
    return jsonify(max_forecast_2deci)


if __name__ == "__main__":
  app.run(host="0.0.0.0")