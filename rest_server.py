from flask import Flask
import flask
import json


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

    @staticmethod
    @app.route("/currency/<currency>")
    def get_currency(currency):
        response = JsonResponse(json.dumps({currency:"simple get"}))
        return response.prepare_response()

    @staticmethod
    @app.route("/currency/forecast/<currency>")
    def forecast_currency(currency):
        response = JsonResponse(json.dumps({currency:"forecast"}))
        return response.prepare_response()

    @staticmethod
    def run_server():
        RestServer.app.run()


if __name__ == '__main__':
    server = RestServer()
    server.run_server()