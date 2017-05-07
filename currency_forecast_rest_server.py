from flask import Flask
from flask import request
from utils.dataharvesters import FixerClient
import flask
import json
import argparse


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
    fixer_client = FixerClient()

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
        fixer_response = RestServer.fixer_client.pull_currency_value(base=currency)
        response = JsonResponse(json.dumps({currency:fixer_response["rates"][output_currency.upper()]}))
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
        supported_methods = ["method1", "method2"]
        forecast_method = request.args.get('method')
        if forecast_method==None:
            forecast_method=supported_methods[0]
        if not (forecast_method in supported_methods):
            return flask.Response(status=404)
        fixer_response = RestServer.fixer_client.pull_currency_value(base=currency)
        currency_value = fixer_response["rates"][output_currency.upper()]*2
        response = JsonResponse(json.dumps({currency: currency_value, "method":forecast_method}))
        return response.prepare_response()

    @staticmethod
    def run_server(port_to_listen):
        RestServer.app.run(host='0.0.0.0', port=port_to_listen)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Runs rest server for forecast currency')
    argparser.add_argument('--port', dest='port', default=5000)
    args = argparser.parse_args()

    server = RestServer()
    server.run_server(args.port)