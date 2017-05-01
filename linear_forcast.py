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

import json, requests
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

from utils.dataharvesters import pull_from_nbp


def linear_extrapolation(currency_code, recent_weeks = "5", week_to_predict = 1):
    x = np.array(range(int(recent_weeks)))
    y = pull_from_nbp(currency_code, recent_weeks)
    model = LinearRegression()
    model.fit(x.reshape(len(x), 1), y)
    #  To plot data
    #  coeff = model.coef_
    #  print (coeff)
    #  plt.scatter(x, y, color='b')
    #  plt.scatter(week_to_predict + int(recent_weeks), model.predict(week_to_predict), color='r')
    #  plt.show()
    return model.predict(week_to_predict + int(recent_weeks))

#testing 
# print (linear_extrapolation("SZL"))

