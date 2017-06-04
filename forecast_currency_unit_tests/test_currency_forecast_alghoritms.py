import currency_forecast_alghoritms
import unittest
from unittest.mock import patch
from utils.dataharvesters import FixerClient
import json


class CurrencyAlghoritmsTest(unittest.TestCase):
    @patch('utils.dataharvesters.FixerClient.pull_currency_value')
    def test_ppp_method(self, mock_fixer):
        mock_fixer.side_effect = [json.loads("{\"rates\":{\"PLN\":4}}")]

        predicted_value = currency_forecast_alghoritms.purchasing_power_parity("PLN")

        self.assertEquals(4.028, predicted_value)