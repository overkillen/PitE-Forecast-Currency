from flask import Flask
from flask import request

from currency_forecast_alghoritms import recurrent_neural_network, purchasing_power_parity, arima_prediction, \
    linear_regression
from utils.dataharvesters import FixerClient, HourlyCollector
import flask
import json
import argparse
import threading
import time


class JsonResponse:
    json_content_type = "application/json"

    def __init__(self, data):
        self.data = data

    def prepare_response(self):
        response = flask.Response(self.data)
        response.headers['Content-Type'] = self.json_content_type
        return response


class RestServer:
    app = Flask("Rest Server")
    precomputed = -1

    @staticmethod
    def generate_response_for_the_same_currencies(currency):
        return JsonResponse(json.dumps({currency:1})).prepare_response()


    @staticmethod
    @app.route("/")
    def index():
        return "Currency forecast"

    @staticmethod
    @app.route("/currency/actual/<currency>/<output_currency>")
    def get_currency(currency, output_currency):
        """
           Returns actual currency value in desired currency(for today).
           Example: GET /currency/actual/usd/pln
                    Returns: actual USD currency value in PLN e.g. {"usd":3.99}
        """
        if currency==output_currency:
            return RestServer.generate_response_for_the_same_currencies(currency)
        else:
            response = HourlyCollector().pull_data(output_currency)
            response = JsonResponse(json.dumps({currency:response[-1]}))
            return response.prepare_response()

    @staticmethod
    @app.route("/currency/forecast/<currency>/<output_currency>")
    def forecast_currency(currency, output_currency):
        """
            Returns currency forecast in desired output currency. You can specify method in 'method' parameter
            Example: GET /currency/forecast/usd/pln
                    GET /currency/forecast/usd/pln?method=better_method
                    Returns: Currency forecast in desired output currency e.g. {"usd:3.99, "method":"better_method"}
        """
        if currency==output_currency:
            return RestServer.generate_response_for_the_same_currencies(currency)
        else:
            supported_methods = ["ppp", "lstm", "arima", "lin"]
            forecast_method = request.args.get('method')
            if forecast_method==None:
                forecast_method=supported_methods[0]
            if not (forecast_method in supported_methods):
                return flask.Response(status=404)
            currency_value = RestServer.handle_supported_methods(currency, forecast_method, output_currency,
                                                                 supported_methods)
            response = JsonResponse(json.dumps({currency: currency_value, "method":forecast_method}))
            return response.prepare_response()

    @staticmethod
    def handle_supported_methods(currency, forecast_method, output_currency, supported_methods):
        currency_value = -1
        if forecast_method == supported_methods[0]:
            currency_value = purchasing_power_parity(currency, output_currency)
        elif forecast_method == supported_methods[1]:
            currency_value = RestServer.precomputed
        elif forecast_method == supported_methods[2]:
            currency_value = arima_prediction(output_currency)
        else:
            currency_value = linear_regression()
        return currency_value

    @staticmethod
    def run_server(port_to_listen):
        RestServer.app.run(host='0.0.0.0', port=port_to_listen)


def update_lstm():
    while True:
        RestServer.precomputed = recurrent_neural_network("PLN")
        time.sleep(3600)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Runs rest server for forecast currency')
    argparser.add_argument('--port', dest='port', default=5000)
    args = argparser.parse_args()
    updater = threading.Thread(target=update_lstm)
    updater.daemon = True
    updater.start()
    server = RestServer()
    server.run_server(args.port)