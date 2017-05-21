import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
import numpy


class CurrencyLSTM:
    def __init__(self, data):
        self.look_back = 1
        self.trainX, self.trainY = self.create_dataset(data, self.look_back)

    def create_dataset(self, dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i:(i + look_back)]
            dataX.append(a)
            dataY.append(dataset[i + look_back])
        return numpy.array(dataX), numpy.array(dataY)

    def predict(self, next_probe):
        to_predict = np.array([[next_probe]])

        scaler = MinMaxScaler(feature_range=(0, 1))
        trainX = scaler.fit_transform(self.trainX)
        trainY = scaler.fit_transform(self.trainY)
        to_predict = scaler.fit_transform(to_predict)

        to_predict = np.reshape(to_predict, (1, 1, 1))
        trainX = np.reshape(trainX, (len(trainX), 1, 1))
        model = Sequential()
        model.add(LSTM(2, input_shape=(1, self.look_back), stateful=True, batch_size=1))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainX, trainY, epochs=300, batch_size=1, verbose=10)

        return scaler.inverse_transform(model.predict(to_predict))[0][0].item()


