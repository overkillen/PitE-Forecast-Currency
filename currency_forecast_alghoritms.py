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

import json

import numpy as np
import requests
from scipy import interpolate

import keras
import matplotlib.pyplot as plt
from currency_lstm import CurrencyLSTM
from sklearn.linear_model import LinearRegression
from utils.dataharvesters import FixerClient, HourlyCollector, NBPClient

FIXER_CLIENT = FixerClient()

def polynomial_extrapolation(x, y):
    params = np.polyfit(x, y, len(x))
    next_arg = max(x) + 1
    return sum(next_arg * i for i in params)

def polynomial_extrapolation2(x, y):
    return interpolate.interp1d(x, y, fill_value="extrapolate")

def linear_regression(currency_code, recent_weeks = "5", week_to_predict = 1):
    x = np.array(range(int(recent_weeks)))
    y = NBPClient().pull_currency_value(currency_code, recent_weeks)
    model = LinearRegression()
    model.fit(x.reshape(len(x), 1), y)
    #  To plot data
    #  coeff = model.coef_
    #  print (coeff)
    #  plt.scatter(x, y, color='b')
    #  plt.scatter(week_to_predict + int(recent_weeks), model.predict(week_to_predict), color='r')
    #  plt.show()
    return model.predict(week_to_predict + int(recent_weeks))


# TO IMPLEMENT  http://www.investopedia.com/articles/forex/11/4-ways-to-forecast-exchange-rates.asp
def purchasing_power_parity(base_currency, output_currency):
    base_inflation = 2
    output_inflation = 4
    inflation_difference = output_inflation - base_inflation
    response = FIXER_CLIENT.pull_currency_value(base=base_currency)
    output_currency_value = response["rates"][output_currency.upper()]
    return (1+inflation_difference/100)*output_currency_value


def arma_prediction():
    return 0


#example http://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
def recurrent_neural_network( output_currency):
    client = HourlyCollector()
    data = np.array(client.pull_data(output_currency))
    lstm = CurrencyLSTM(data)
    return lstm.predict()


#testing 
# print (linear_extrapolation("SZL"))

