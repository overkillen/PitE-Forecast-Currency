'''
function linear_extrapolation uses linear extrapolation to calculate future exchange rate
inputs:
        currency_code, string, a three- letter currency code (ISO 4217 standard)
        recent_days, string, A number determining how many weeks back the linear extrapolation is calculated from
        week_to_predict, string, A week in the future for which we count the exchange rate
output:
        float, currency exchange rate for week_to_predict

requirement scikit-learn, matplotlib - optional for plots
'''

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


def linear_regression(x, y, week_to_predict=1, **kwargs):
    x = np.array(x)
    y = np.array(y)
    model = LinearRegression()
    model.fit(x.reshape(len(x), 1), y)
    return model.predict(week_to_predict + int(len(x)))


# http://www.investopedia.com/articles/forex/11/4-ways-to-forecast-exchange-rates.asp
def purchasing_power_parity(base_currency, output_currency, client=FixerClient()):
    response = client.pull_currency_value(base=base_currency)
    output_currency_value = response["rates"][output_currency.upper()]
    return purchasing_power_parity_algorithm(output_currency_value)


def purchasing_power_parity_algorithm(output_currency_value, base_inflation=2,
                                      output_inflation=4):
    inflation_difference = output_inflation - base_inflation
    return (1+inflation_difference/100)*output_currency_value


def arima_prediction(output_currency, client=HourlyCollector()):
    data = client.pull_data(output_currency)
    model = ARIMA(data, order=(2, 1, 0))
    model_fit = model.fit(disp=0)
    return model_fit.forecast()[0]


# example http://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
def recurrent_neural_network(output_currency, client=HourlyCollector()):
    data = np.array(client.pull_data(output_currency))
    lstm = CurrencyLSTM(data)
    return lstm.predict()

