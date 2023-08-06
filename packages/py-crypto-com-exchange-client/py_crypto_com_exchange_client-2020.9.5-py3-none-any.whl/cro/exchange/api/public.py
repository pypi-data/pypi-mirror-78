import logging
from logging import INFO
from urllib.parse import urljoin

import requests

from cro.exchange.api.base import BaseCryptoComClient


class PublicAPIClient(BaseCryptoComClient):

    def __init__(self, is_sandbox=True):
        super(PublicAPIClient, self).__init__(is_sandbox=is_sandbox)
        self._public_api_url = urljoin(self._root_url, 'public/')

    def get_instruments(self):
        """
        Gets the available instruments list
        :return: dictionary of instruments, format below:
        {
            'id': id,
            'method': 'public/get-instruments',
            'code': response code,
            'result': {
                'instruments': [
                    {
                        'instrument_name': 'name (ex. ADA_BTC)',
                        'quote_currency': 'BTC', '
                        'base_currency': 'ADA',
                        'price_decimals': 8,
                        'quantity_decimals': 0
                    }
                ]
            }
        }
        """
        instr_url = urljoin(self._public_api_url, 'get-instruments')
        response = requests.get(instr_url)
        return response.json()

    def get_book(self, instrument_name, depth=10):
        """
        Gets the current book for the given instrument name
        :param instrument_name: the instrument name (ex. ADA_BTC)
        :param depth: the number of entries requested
        :return: the book at the time of request, format below:
        {
            'code': 0,
            'method': 'public/get-book',
            'result': {
                'instrument_name': 'BTC_USDT',
                'depth': 10,
                'data': [
                    {
                        'bids': [
                            [10001.0, 1.936071, 2],
                            [10000.0, 0.0001, 1],
                            [9638.19, 0.112565, 1],
                        ],
                        'asks': [
                            [11111.0, 0.67, 1],
                            [12000.0, 1.0, 1],
                        ],
                        't': 1597609520039
                    }
                ]
            }
        }
        """
        book_url = urljoin(self._public_api_url, 'get-book')
        response = requests.get(book_url, params={'instrument_name': instrument_name, 'depth': depth})
        return response.json()

    def get_ticker(self, instrument_name=None):
        """
        Gets the public tickers for the given instrument
        :param: instrument_name: the instrument name (optional)
        :return:
        {
            'code': 0,
            'method': 'public/get-ticker',
            'result': {
                'data': [
                    {
                        'i': 'Instrument Name, e.g. BTC_USDT, ETH_CRO, etc.',
                        'b': 'The current best bid price, null if there aren't any bids',
                        'k': 'The current best ask price, null if there aren't any asks',
                        'a': 'The price of the latest trade, null if there weren't any trades',
                        't': 'Timestamp of the data',
                        'v': 'The total 24h traded volume',
                        'h': 'Price of the 24h highest trade',
                        'l': 'Price of the 24h lowest trade, null if there weren't any trades',
                        'c': '24-hour price change, null if there weren't any trades',
                    },
                ],
            },
        }
        """
        ticker_url = urljoin(self._public_api_url, 'get-ticker')
        params = {'instrument_name': instrument_name} if instrument_name else dict()
        response = requests.get(ticker_url, params=params)
        return response.json()

    def get_trades(self, instrument_name=None):
        """
        Fetches the public trades for a particular instrument
        :param: instrument_name: the instrument name (optional)
        :return:
        {
            'code': 0,
            'method': 'public/get-trades',
            'result': {
                'instrument_name': 'BTC_USDT',
                'data': [
                    {
                        'p': Trade price,
                        'q': Trade quantity,
                        's': Side ("buy" or "sell"),
                        'd': Trade ID,
                        't': Trade timestamp,
                        'dataTime': Reserved. Can be ignored,
                    },
                ],
            }
        }
        """
        trades_url = urljoin(self._public_api_url, 'get-trades')
        params = {'instrument_name': instrument_name} if instrument_name else dict()
        response = requests.get(trades_url, params=params)
        return response.json()


if __name__ == '__main__':
    logging.basicConfig(level=INFO)
    api = PublicAPIClient()
    print(api.get_instruments())
    print(api.get_book('BTC_USDT'))
    print(api.get_ticker('BTC_USDT'))
    print(api.get_trades('BTC_USDT'))
