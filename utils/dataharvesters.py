import aiohttp
import asyncio
from datetime import datetime, timedelta
from requests import HTTPError
import requests

from .exceptions import DataPullError, InvalidInput


def raise_or_leave(resp):
    """
    Raise DataPullError if an HTTPError eccured, else return that response
    """
    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise DataPullError(str(e))
    return resp


class FixerClient:
    FIXER_URL = 'http://api.fixer.io/'

    async def _pull_for_one_day(self, currency_code, date=None, base='PLN'):
        """
        """
        if date is None:
            date = 'latest'
        else:
            date = date.strftime("%Y-%m-%d")
        """
        Date is a datetime.date object
        """
        url = 'http://api.fixer.io/{}'.format(date)
        params = {'base': currency_code}
        params['symbols'] = base
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                raise_or_leave(resp)
                return await resp.json()

    def pull_currency_value(self, currency_code, days, base='PLN'):
        if days < 1:
            return []
        loop = asyncio.get_event_loop()
        tasks = [self._pull_for_one_day(
                        currency_code, datetime.today() - timedelta(days=i), base)
                        for i in range(days)]
        results =  [t.result()
                    for t in loop.run_until_complete(asyncio.wait(tasks))[0]]
        return [i['rates'][base] for i in sorted(results, key=lambda x: x['date'])]


class NBPClient:
    NBP_URL = "http://api.nbp.pl/api/exchangerates/rates/"
    # Data in nbp api is splited into 2 categories
    CURRENCY_TO_CATEGORY = {
            'THB': 'A', 'USD': 'A', 'AUD': 'A', 'HKD': 'A', 'CAD': 'A', 'NZD': 'A',
            'SGD': 'A', 'EUR': 'A', 'HUF': 'A', 'CHF': 'A', 'GBP': 'A', 'UAH': 'A',
            'JPY': 'A', 'CZK': 'A', 'DKK': 'A', 'ISK': 'A', 'NOK': 'A', 'SEK': 'A',
            'HRK': 'A', 'RON': 'A', 'BGN': 'A', 'TRY': 'A', 'ILS': 'A', 'CLP': 'A',
            'PHP': 'A', 'MXN': 'A', 'ZAR': 'A', 'BRL': 'A', 'MYR': 'A', 'RUB': 'A',
            'IDR': 'A', 'INR': 'A', 'KRW': 'A', 'CNY': 'A', 'XDR': 'A',
            'AFN': 'B', 'MGA': 'B', 'PAB': 'B', 'ETB': 'B', 'VEF': 'B', 'BOB': 'B',
            'CRC': 'B', 'SVC': 'B', 'NIO': 'B', 'GMD': 'B', 'MKD': 'B', 'DZD': 'B',
            'BHD': 'B', 'IQD': 'B', 'JOD': 'B', 'KWD': 'B', 'LYD': 'B', 'RSD': 'B',
            'TND': 'B', 'MAD': 'B', 'AED': 'B', 'STD': 'B', 'BSD': 'B', 'BBD': 'B',
            'BZD': 'B', 'BND': 'B', 'FJD': 'B', 'GYD': 'B', 'JMD': 'B', 'LRD': 'B',
            'NAD': 'B', 'SRD': 'B', 'TTD': 'B', 'XCD': 'B', 'SBD': 'B', 'VND': 'B',
            'AMD': 'B', 'CVE': 'B', 'AWG': 'B', 'BIF': 'B', 'XOF': 'B', 'XAF': 'B',
            'XPF': 'B', 'DJF': 'B', 'GNF': 'B', 'KMF': 'B', 'CDF': 'B', 'RWF': 'B',
            'EGP': 'B', 'GIP': 'B', 'LBP': 'B', 'SDG': 'B', 'SYP': 'B', 'GHS': 'B',
            'HTG': 'B', 'PYG': 'B', 'ANG': 'B', 'PGK': 'B', 'LAK': 'B', 'MWK': 'B',
            'ZMW': 'B', 'AOA': 'B', 'MMK': 'B', 'GEL': 'B', 'MDL': 'B', 'ALL': 'B',
            'HNL': 'B', 'SLL': 'B', 'SZL': 'B', 'LSL': 'B', 'AZN': 'B', 'MZN': 'B',
            'NGN': 'B', 'ERN': 'B', 'TWD': 'B', 'PEN': 'B', 'MRO': 'B', 'TOP': 'B',
            'MOP': 'B', 'ARS': 'B', 'DOP': 'B', 'COP': 'B', 'UYU': 'B', 'BWP': 'B',
            'GTQ': 'B', 'IRR': 'B', 'YER': 'B', 'QAR': 'B', 'OMR': 'B', 'SAR': 'B',
            'KHR': 'B', 'BYN': 'B', 'LKR': 'B', 'MVR': 'B', 'MUR': 'B', 'NPR': 'B',
            'PKR': 'B', 'SCR': 'B', 'KGS': 'B', 'TJS': 'B', 'UZS': 'B', 'KES': 'B',
            'SOS': 'B', 'TZS': 'B', 'UGX': 'B', 'BDT': 'B', 'WST': 'B', 'KZT': 'B',
            'MNT': 'B', 'VUV': 'B', 'BAM': 'B',
            }

    def pull_currency_value(self, currency_code, days):
        table_type = NBPClient.CURRENCY_TO_CATEGORY.get(currency_code)
        if table_type is None:
            raise InvalidInput("Invalid currency code: {}".format(currency_code))
        response = requests.get(
            "{}{}/{}/last/{}?format=json".format(NBPClient.NBP_URL, table_type, currency_code, days))
        raise_or_leave(response)
        response = response.json()
        return [rates["mid"] for rates in response["rates"]]

