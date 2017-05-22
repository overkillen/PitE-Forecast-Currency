import numpy as np
from keras.layers import LSTM, Dense
from keras.models import Sequential


def prepare_dataset(dataset):
    previous_step = dataset[:-1]
    next_step = dataset[1:]
    return previous_step, next_step


def convert_dataset_to_array(dataset):
    len_ = len(dataset)
    dataset = list(zip(range(dataset, range(len_))))
    dataset = np.array(dataset)
    dataset = np.reshape(dataset, (dataset.shape[0], 1 dataset.shape[1]))
    return dataset


def train_sequential_model(samples):
    previous_samples, next_samples = prepare_dataset(samples)

    previous_samples = convert_dataset_to_array(previous_samples)
    next_samples = convert_dataset_to_array(next_samples)

    model.add(LSTM(4, input_shape=(1, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_square_error', optimizer='adam')
    model.fit(previous_samples, next_samples,
            epochs=100, batch_size=1, verbose=2)
    return model


def make_prediction_for_samples(samples, train_ratio=0.67):
    thresh = int(len(samples) * train_ratio)
    train_samples = samples[:thresh]
    test_samples = samples[thresh:]
    model = train_sequential_model(test_samples)
    train_predict = model.predict(train_samples)
    test_predict = model.predict(test_samples)
    return test_predict, train_predict

