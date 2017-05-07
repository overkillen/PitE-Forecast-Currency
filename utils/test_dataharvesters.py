import unittest
import requests
from utils.dataharvesters import raise_or_leave
from utils.exceptions import DataPullError


class DataharvestersTest(unittest.TestCase):
    def test_data_pull_error(self):
        response = requests.Response()
        response.status_code = 404

        self.assertRaises(DataPullError, raise_or_leave, response)
