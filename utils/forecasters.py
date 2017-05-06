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

