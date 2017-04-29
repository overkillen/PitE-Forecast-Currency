from flask import Flask
from flask import request
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

    @staticmethod
    @app.route("/")
    def index():
        return "Currency forecast"

    """
    Returns actual currency value (for today).
    Example: GET /currency/actual/usd
             Returns: {"usd:3.99"}
    """
    @staticmethod
    @app.route("/currency/actual/<currency>")
    def get_currency(currency):
        response = JsonResponse(json.dumps({currency:"actual"}))
        return response.prepare_response()

    """
       Returns currency forecast. You can specify method in 'method' parameter
       Example: GET /currency/forecast/usd
                GET /currency/forecast/usd?method=better_method
                Returns: {"usd:3.99, "method":"better_method"}
       """
    @staticmethod
    @app.route("/currency/forecast/<currency>")
    def forecast_currency(currency):
        forecast_method = request.args.get('method')
        if forecast_method==None:
            forecast_method="method1"
        response = JsonResponse(json.dumps({currency:"forecast", "method":forecast_method}))
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