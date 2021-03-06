import currency_forecast_alghoritms
import unittest
from unittest.mock import patch
from utils.dataharvesters import FixerClient
import json


class CurrencyAlghoritmsTest(unittest.TestCase):
    @patch('utils.dataharvesters.HourlyCollector.pull_data')
    def test_ppp_method(self, mock_fixer):
        mock_fixer.side_effect = [[4]]

        predicted_value = currency_forecast_alghoritms.purchasing_power_parity("USD", "PLN")

        self.assertEquals(4.004, predicted_value)