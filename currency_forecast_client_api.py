import requests


class CurrencyForecastClient:
    def __init__(self, url, port=443):
        self.url = url
        self.port = port
        self.address = "{}:{}".format(url, port)

    def get_hello_message(self):
        response = requests.get(self.address)
        return response.json()

    """
        Returns as json: {"currency_name":actual_currency_value}
    """
    def get_actual_value_for_currency(self, currency):
        response = requests.get("{}/currency/actual/{}".format(self.address, currency))
        return response.json()

    """
       Returns as json: {"currency_name":forecast_currency_value, "method":"forecast_method_name"}
    """
    def forecast_currency(self, currency, method="method1"):
        response = requests.get("{}/currency/forecast/{}?method={}".format(self.address, currency, method))
        return response.json()
