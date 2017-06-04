from statsmodels.tsa.arima_model import ARIMA
import numpy as np
from scipy import interpolate

from currency_lstm import CurrencyLSTM
from sklearn.linear_model import LinearRegression
from utils.dataharvesters import FixerClient, HourlyCollector


def polynomial_extrapolation(x, y):
    params = np.polyfit(x, y, len(x))
    next_arg = len(x) + 1
    return sum(next_arg**n * a for n, a in enumerate(reversed(params)))


def polynomial_extrapolation2(x, y):
    return interpolate.interp1d(x, y, fill_value="extrapolate")


def linear_regression(output_currency="PLN", client=HourlyCollector(), week_to_predict=1, **kwargs):
    data = client.pull_data(output_currency)
    x = np.array(range(0, len(data)))
    y = np.array(data)
    model = LinearRegression()
    model.fit(x.reshape(len(x), 1), y)
    return model.predict(week_to_predict + int(len(x))).item()


# http://www.investopedia.com/articles/forex/11/4-ways-to-forecast-exchange-rates.asp
def purchasing_power_parity(base_currency="USD", output_currency="PLN", client=HourlyCollector()):
    response = client.pull_data(output_currency)
    output_currency_value = response[-1]
    return purchasing_power_parity_algorithm(output_currency_value)


def purchasing_power_parity_algorithm(output_currency_value, base_inflation=2,
                                      output_inflation=2.7):
    inflation_difference = output_inflation - base_inflation
    return (1+inflation_difference/100)*output_currency_value


def arima_prediction(output_currency, client=HourlyCollector(), base_currency="USD"):
    data = client.pull_data(output_currency)
    model = ARIMA(data, order=(2, 1, 0))
    model_fit = model.fit(disp=0)
    return model_fit.forecast()[0].item()


# example http://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
def recurrent_neural_network(output_currency, client=HourlyCollector(), base_currency="USD"):
    data = np.array(client.pull_data(output_currency))
    lstm = CurrencyLSTM(data)
    return lstm.predict()

