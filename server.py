import pandas as pd
import json
import numpy as np
import math
from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, request,jsonify
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
 

app = Flask(__name__)
df = pd.read_csv('.\Machine_Learning\Dataset\server_two-hundred-fourty-second-wbgt.csv')
current_array = df.to_numpy()

NUMBER_OF_DAYS =0.5
NUMBER_OF_DATA_POINT =  math.floor((NUMBER_OF_DAYS * 86400)/240)

NUMBER_OF_FORECAST_STEPS = 5

current_array = current_array[len(current_array) - NUMBER_OF_DATA_POINT - 1:]
train_size = math.floor(0.8*NUMBER_OF_DATA_POINT)
test_size =math.floor(NUMBER_OF_DATA_POINT)

wbt_high_risk_black = 28.0
wbt_high_risk_red = 27.0
wbt_medium_risk_yellow = 26.0
wbt_low_risk_green = 25.0
wbt_low_risk_white =  24.9


@app.route("/", methods=['GET'])
def hello():
    return 'Hello World!'

@app.route("/forecast", methods=['GET'])
def return_forecast_data():
    arima_value = arima()
    print({'forecast_wbgt' : arima_value.json})
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

@app.route("/decision_tree", methods=['POST'])
def get_decision_tree():
    data = request.json
    sensor_data = data["sensor_wbgt"]
    print(data["sensor_wbgt"])
    decisionTreeLabel = decisionTree(sensor_data)
    print(decisionTreeLabel)
    return jsonify({'decision_tree_label' : decisionTreeLabel})

def arima():
    train = current_array[0:train_size]
    #test = current_array[train_size:test_size]
    model = ARIMA(train, order=(1,1,5))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=NUMBER_OF_FORECAST_STEPS)
    max_forecast = max(forecast)
    max_forecast_2deci = float("{:.2f}".format(max_forecast))
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
  app.run(host="0.0.0.0")