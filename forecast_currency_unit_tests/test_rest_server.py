import unittest
import rest_server
import json


class TestRestServer(unittest.TestCase):
    def setUp(self):
        rest_server.RestServer.app.config['TESTING'] = True
        self.app = rest_server.RestServer.app.test_client()

    def test_welcome_message(self):
        expected_welcome_message = "Currency forecast"
        response = self.app.get('/')
        self.assertEqual(expected_welcome_message, response.data.decode())

    def test_forecast_method_when_method_parameter_missing(self):
        default_method = "method1"
        response = self.app.get('/currency/forecast/usd')
        self.assertEqual(default_method, json.loads(response.data.decode())['method'])

    def test_forecast_method_when_method_parameter_present(self):
        default_method = "abcdefg"
        response = self.app.get('/currency/forecast/usd?method=abcdefg')
        self.assertEqual(default_method, json.loads(response.data.decode())['method'])
