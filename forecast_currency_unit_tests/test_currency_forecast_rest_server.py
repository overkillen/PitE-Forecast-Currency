import unittest
from currency_forecast_rest_server import JsonResponse
import currency_forecast_rest_server
import json


class TestRestServer(unittest.TestCase):
    def setUp(self):
        currency_forecast_rest_server.RestServer.app.config['TESTING'] = True
        self.app = currency_forecast_rest_server.RestServer.app.test_client()

    def test_welcome_message(self):
        expected_welcome_message = "Currency forecast"
        response = self.app.get('/')
        self.assertEqual(expected_welcome_message, response.data.decode())

    def test_actual_currency_value(self):
        response = self.app.get('/currency/actual/usd/pln')
        self.assertTrue("usd" in json.loads(response.data.decode()))

    def test_forecast_method_when_method_parameter_missing(self):
        default_method = "ppp"
        response = self.app.get('/currency/forecast/usd/pln')
        self.assertEqual(default_method, json.loads(response.data.decode())['method'])
        self.assertTrue("usd" in json.loads(response.data.decode()))

    def test_forecast_method_when_method_parameter_present(self):
        default_method = "arma"
        response = self.app.get('/currency/forecast/usd/pln?method=arma')
        self.assertEqual(default_method, json.loads(response.data.decode())['method'])
        self.assertTrue("usd" in json.loads(response.data.decode()))

    def test_forecast_unsupported_method(self):
        response = self.app.get('/currency/forecast/usd/pln?method=abcdefg')
        self.assertEqual(404, response.status_code)

    def test_currencies_are_the_same(self):
        response = self.app.get('/currency/forecast/usd/usd')
        self.assertEqual(1, json.loads(response.data.decode())['usd'])


class JsonResponseTest(unittest.TestCase):

    def test_json_header_in_response(self):
        json_response = JsonResponse(json.dumps("{\"a\":1}"))
        header = json_response.prepare_response().content_type
        self.assertEqual("application/json", header)
