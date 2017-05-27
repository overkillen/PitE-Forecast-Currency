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
import json
import numpy as np
import requests
from scipy import interpolate

import keras
import matplotlib.pyplot as plt
from currency_lstm import CurrencyLSTM
from sklearn.linear_model import LinearRegression
from utils.dataharvesters import FixerClient, HourlyCollector, NBPClient, CURRENCY_INFLATION

FIXER_CLIENT = FixerClient()

def polynomial_extrapolation(x, y):
    params = np.polyfit(x, y, len(x))
    next_arg = len(x) + 1
    return sum(next_arg**n * a for n, a in enumerate(reversed(params)))

def polynomial_extrapolation2(x, y):
    return interpolate.interp1d(x, y, fill_value="extrapolate")

def linear_regression(output_currency):
    y = HourlyCollector().pull_data(output_currency)
    x = np.array(range(len(y)))
    model = LinearRegression()
    model.fit(x.reshape(len(x), 1), y)
    return model.predict(len(y) + 1)


# TO IMPLEMENT  http://www.investopedia.com/articles/forex/11/4-ways-to-forecast-exchange-rates.asp
def purchasing_power_parity(output_currency):
    base_currency = "USD"
    inflation_difference = CURRENCY_INFLATION[output_currency] - CURRENCY_INFLATION[base_currency]
    response = HourlyCollector().pull_data(output_currency)
    output_currency_value = response[-1]
    return (1+inflation_difference/100)*output_currency_value


def arima_prediction(output_currency):
    data = HourlyCollector().pull_data(output_currency)
    model = ARIMA(data, order =(2, 1, 0))
    model_fit = model.fit(disp=0)
    return model_fit.forecast()[0]
    

#example http://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
def recurrent_neural_network( output_currency):
    client = HourlyCollector()
    data = np.array(client.pull_data(output_currency))
    lstm = CurrencyLSTM(data)
    return lstm.predict()


#testing 
# print (linear_extrapolation("SZL"))

