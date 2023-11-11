# Time Series Prediction with GRU
import numpy
import matplotlib.pyplot as plt
import pandas as pd
import math
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import GRU
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from pickle import dump

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

#convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
 dataX, dataY = [], []
 for i in range(len(dataset)-look_back-1):
  a = dataset[i:(i+look_back), 0]
  dataX.append(a)
  dataY.append(dataset[i + look_back, 0])
 return numpy.array(dataX), numpy.array(dataY)


# fix random seed for reproducibility
numpy.random.seed(7)


dataset_name = "lanh-su-quan-hoa-ky-hcm"
product_name = "pm25"
file_path = dir_path+'/dataset/data-pm2.5-lanh-su-quan-hcm-20160211-20211203.csv'
dataframe = pd.read_csv(file_path)
dataframe['date'] = pd.to_datetime(dataframe.date, format='%Y-%m-%d', errors='coerce')
dataframe = dataframe.sort_values(by='date') 
print("Dataframe: \n", dataframe)
dataset = numpy.asarray(dataframe[product_name]).reshape(-1,1)
print("MIN=", dataset.min(),"MAX=", dataset.max(),"AVG=", dataset.mean())
print("Dataset: \n", dataset)

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
print("Dataset after scale: \n", dataset)

# split into train and test sets
train_size = int(len(dataset) * 0.7)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

# reshape into X=t and Y=t+1
look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
print("TrainX shape: ", trainX.shape)
print("TrainY shape: ", trainY.shape)

# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# create and fit the GRU network
model = Sequential()
# model.add(GRU(4, input_shape=(1, look_back), return_sequences=True))
model.add(GRU(4, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
print(model.summary())
history = model.fit(trainX, trainY, epochs=1000, batch_size=10, verbose=2,
          validation_data=(testX, testY))

score = model.evaluate(testX, testY, verbose=0)
print('score: test score = ', score)

# save the model
model.save(dir_path+'/models-py/rnn-GRU-'+product_name)
# save the scaler
dump(scaler, open(dir_path+'/models-py/rnn-GRU-'+product_name+'/scaler.pkl', 'wb'))

plt.plot(history.history['loss'])

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)


# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

test_Y = testY[0][len(testY[0])-15:len(testY[0])-1]
test_Ypred = testPredict[len(testPredict)-15:len(testPredict)-1]
plt.subplots(figsize=(10, 5))
plt.title(product_name.upper() + " - Forecast vs Actual", fontsize=14)
plt.plot(pd.Series(numpy.ravel(test_Y)), "bs-", markersize=3, label="Actual")
plt.plot(pd.Series(numpy.ravel(test_Ypred)), "ro-", markersize=3, label="Forecast")
plt.legend(loc="best")
plt.xlabel("Days")
plt.ylim([-50,300])
plt.show()

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.8f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.8f RMSE' % (testScore))

# # shift train predictions for plotting
# trainPredictPlot = numpy.empty_like(dataset)
# trainPredictPlot[:, :] = numpy.nan
# trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# # shift test predictions for plotting
# testPredictPlot = numpy.empty_like(dataset)
# testPredictPlot[:, :] = numpy.nan
# testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict

# # plot baseline and predictions
# plt.plot(scaler.inverse_transform(dataset),"b-", label="Actual")
# plt.plot(trainPredictPlot,"y-", label="Train pred")
# plt.plot(scaler.inverse_transform(testY)[0],"b-", label="Actual")
# plt.plot(testPredictPlot, "g-", label="Test pred")
# plt.legend(loc="best")
# # plt.ylim([-0.02,0.02])
# plt.show()