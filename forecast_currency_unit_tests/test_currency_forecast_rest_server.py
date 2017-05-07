import unittest
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
        default_method = "method1"
        response = self.app.get('/currency/forecast/usd/pln')
        self.assertEqual(default_method, json.loads(response.data.decode())['method'])

    def test_forecast_method_when_method_parameter_present(self):
        default_method = "method2"
        response = self.app.get('/currency/forecast/usd/pln?method=method2')
        self.assertEqual(default_method, json.loads(response.data.decode())['method'])

    def test_forecast_unsupported_method(self):
        response = self.app.get('/currency/forecast/usd?method=abcdefg')
        self.assertEqual(404, response.status_code)
