import multiprocessing
import pandas as pd
import json
import numpy as np
import math
import time
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import Dropout, LeakyReLU
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from flask import Flask, request,jsonify
from sklearn import tree
 

app = Flask(__name__)
MONTHS = 1
NUMBER_OF_DATA_POINT = math.floor(MONTHS * 4 * 7 *24 * (60/2))
df = pd.read_csv('Machine_Learning\Dataset\hundred-twenty-second-wbgt.csv')
#current_array = df.to_numpy()
df_timeseries_mean = df.rolling(window=1).mean()
current_array = np.array(df_timeseries_mean[-NUMBER_OF_DATA_POINT:])

ARIMA_PARAMETERS = (5,1,0)

NUMBER_OF_FORECAST_STEPS = 5
NUMBER_OF_MODELS = 4

#current_array = current_array[len(current_array) - NUMBER_OF_DATA_POINT - 1:]
#current_array = current_array[:NUMBER_OF_DATA_POINT]
train_size = math.floor(0.8*NUMBER_OF_DATA_POINT)
test_size =math.floor(NUMBER_OF_DATA_POINT)

wbt_high_risk_black = 28.0
wbt_high_risk_red = 27.0
wbt_medium_risk_yellow = 26.0
wbt_low_risk_green = 25.0
wbt_low_risk_white =  24.9

# model = Sequential()
# model.add(LSTM(128, activation='relu', input_shape=(5,1), return_sequences=True))
# model.add(LSTM(64, activation='relu', return_sequences=False))
# model.add(RepeatVector(5))
# model.add(LSTM(64, activation='relu', return_sequences=True))
# model.add(LSTM(128, activation='relu', return_sequences=True))
# model.add(TimeDistributed(Dense(1)))
# model.compile(optimizer='adam', loss='mse')
    

@app.route("/", methods=['GET'])
def hello():
    return 'Hello World!'

@app.route("/forecast", methods=['GET'])
def return_forecast_data():
    arima_return_value = multiprocessing.Value("d", 0.0, lock=False)
    holt_return_value = multiprocessing.Value("d", 0.0, lock=False)
    ses_return_value = multiprocessing.Value("d", 0.0, lock=False)
    # lstm_return_value = multiprocessing.Value("d", 0.0, lock=False)
    # lstm_value = multiprocessing.Process(target=lstm, args=[lstm_return_value])
    arima_value = multiprocessing.Process(target=arima, args=[arima_return_value])
    holt_value = multiprocessing.Process(target=holt, args=[holt_return_value])
    ses_value = multiprocessing.Process(target=ses, args=[ses_return_value])
    # lstm_value.start()
    arima_value.start()
    holt_value.start()
    ses_value.start()
    arima_value.join()
    holt_value.join()
    ses_value.join()
    lstm_value = lstm()
    # print("ARIMA =  " + str(arima_return_value.value))
    # print("SES = " + str(ses_return_value.value))
    # print("HOLT = " + str(holt_return_value.value))
    print("LSTM = " + str(lstm_value.json))

    arima_predicted =  float(arima_return_value.value)
    ses_predicted =  float(ses_return_value.value)
    holt_predicted =  float(holt_return_value.value)
    lstm_predicted = float(lstm_value.json)
    
    average_wbgt = (arima_predicted + ses_predicted+holt_predicted+lstm_predicted ) / NUMBER_OF_MODELS
    print("AVERAGE = " + str(average_wbgt))
    #print({'forecast_wbgt' : arima_value.json})
    return jsonify({'forecast_wbgt' : average_wbgt})
    

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
    #print (current_array.shape)
    data = request.json
    print(data["sensor_wbgt"])
    sensor_data = data["sensor_wbgt"]
    update_array = current_array[1:]
    update_array = np.append(update_array,float(sensor_data))
    new_array = np.asarray(update_array)
    current_array = new_array.reshape(len(new_array),1)
    #print (current_array.shape)
    # df_array = df_array.append(data["sensor_wbgt"])
    #return jsonify(data)
    return f'{current_array}'

@app.route("/decision_tree", methods=['POST'])
def get_decision_tree():
    data = request.json
    sensor_data = data["sensor_wbgt"]
    start = time.time()
    for i in range (20):
        print("Loop number " + str(i))
        decisionTreeLabel = decisionTree(sensor_data)
    end = time.time()
    print("Total time taken for 20 loops: " + str(end-start) + " seconds")
    print(decisionTreeLabel)
    return jsonify({'decision_tree_label' : decisionTreeLabel})

def arima(arima_return_value):
    train = current_array[0:train_size]
    #test = current_array[train_size:test_size]
    model = ARIMA(train, order=ARIMA_PARAMETERS)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=NUMBER_OF_FORECAST_STEPS)
    max_forecast = max(forecast)
    max_forecast_2deci = float("{:.2f}".format(max_forecast))
    arima_return_value.value = max_forecast_2deci
    #return jsonify(max_forecast_2deci)

def ses(ses_return_value):
    train = current_array[0:train_size]
    model_fit = SimpleExpSmoothing(train, initialization_method="estimated").fit()
    ses_forecast = model_fit.forecast(NUMBER_OF_FORECAST_STEPS)
    max_forecast = max(ses_forecast)
    max_forecast_2deci = float("{:.2f}".format(max_forecast))
    ses_return_value.value = max_forecast_2deci
    #return jsonify(max_forecast_2deci)

def holt(holt_return_value):
    train = current_array[0:train_size]
    #test = current_array[train_size:test_size]
    model_fit = SimpleExpSmoothing(train, initialization_method="estimated").fit()
    holt_forecast = model_fit.forecast(NUMBER_OF_FORECAST_STEPS)
    max_forecast = max(holt_forecast)
    max_forecast_2deci = float("{:.2f}".format(max_forecast))
    holt_return_value.value = max_forecast_2deci
    #return jsonify(max_forecast_2deci)

def lstm():
    train = current_array[0:train_size]
    test = current_array[train_size:test_size]
    model.fit(train, train, epochs=10, batch_size=300, verbose=0)
    yhat = model.predict(test,verbose=0)
    #print(yhat[-1])
    max_forecast = np.max(yhat[-1])
    max_forecast_2deci = float("{:.2f}".format(max_forecast))
    #print("LSTM:" + str(max_forecast_2deci))
    #return_value.value = max_forecast_2deci
    return jsonify(max_forecast_2deci)


def decisionTree(sensor_wbgt):
    df_clean_data = df.copy()
    df_modified_threshold = df_clean_data.copy() #Clean data before data processing
    df_modified_threshold.columns=['wbgt']
    risk_level = []

    for row in df_modified_threshold.index:
        if(df_modified_threshold['wbgt'][row]>=wbt_high_risk_black):
            risk_level.append('high_black')
        elif((df_modified_threshold['wbgt'][row]>=wbt_high_risk_red) & (df_modified_threshold['wbgt'][row]<wbt_high_risk_black)):
            risk_level.append('high_red')
        elif((df_modified_threshold['wbgt'][row]>=wbt_medium_risk_yellow) & (df_modified_threshold['wbgt'][row]<wbt_high_risk_red)):
            risk_level.append('medium_yellow')
        elif((df_modified_threshold['wbgt'][row]>=wbt_low_risk_green) & (df_modified_threshold['wbgt'][row]<wbt_medium_risk_yellow)):
            risk_level.append('low_green')
        else:
            risk_level.append('low_white')

    df_modified_threshold['risk_level'] = risk_level
    

    X=df_modified_threshold[['wbgt']].to_numpy()

    Y=df_modified_threshold[['risk_level']].to_numpy()
    Y=Y.reshape(-1)
    
    Y = df_modified_threshold['risk_level']
    X = df_modified_threshold.drop(['risk_level'],axis=1)

    clf = tree.DecisionTreeClassifier(criterion='entropy',max_depth=5)
    clf = clf.fit(X, Y)
    DTTraining = df_modified_threshold
    if(float(sensor_wbgt)>=float(wbt_high_risk_black)):            
       predicted_DT_label = 'high_black'
    elif(float(sensor_wbgt)>=float(wbt_high_risk_red) and float(sensor_wbgt)<float(wbt_high_risk_black)):
        predicted_DT_label = 'high_red'
    elif (float(sensor_wbgt)>=float(wbt_medium_risk_yellow) and float(sensor_wbgt) <float(wbt_high_risk_red)):
        predicted_DT_label = 'medium_yellow'
    elif (float(sensor_wbgt)>=float(wbt_low_risk_green) and float(sensor_wbgt) <float(wbt_medium_risk_yellow)):
        predicted_DT_label = 'low_green'
    else:
        predicted_DT_label = 'low_white'

    
    testData = [[sensor_wbgt,predicted_DT_label]]
    testData = pd.DataFrame(testData, columns=DTTraining.columns)
    testX = testData.drop(['risk_level'],axis=1)

    predY = clf.predict(testX)
    predictions = pd.concat([testData,pd.Series(predY,name='Predicted Risk')], axis=1)
    decisionTreeWbgt = predictions['Predicted Risk'].values[0]
    return decisionTreeWbgt

if __name__ == "__main__":
    model = Sequential()
    model.add(LSTM(128, activation='relu', input_shape=(5,1), return_sequences=True))
    model.add(LSTM(64, activation='relu', return_sequences=False))
    model.add(RepeatVector(5))
    model.add(LSTM(64, activation='relu', return_sequences=True))
    model.add(LSTM(128, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(1)))
    model.compile(optimizer='adam', loss='mse')
    app.run(host="0.0.0.0")