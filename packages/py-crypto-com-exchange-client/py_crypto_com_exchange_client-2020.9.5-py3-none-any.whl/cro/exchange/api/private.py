import hashlib
import hmac
import json
import logging
import os
import time
from logging import DEBUG, debug
from urllib.parse import urljoin

import requests

from cro.exchange.api.base import BaseCryptoComClient


class PrivateAPIClient(BaseCryptoComClient):

    def __init__(self, is_sandbox=True):
        """
        Client to access private APIs which needs authentication
        :param is_sandbox: true if need to connect to Crypto.com UAT URL, False otherwise
        """
        super(PrivateAPIClient, self).__init__(is_sandbox=is_sandbox)
        self._private_url = urljoin(self._root_url, 'private/')

    def get_account_summary(self, request_id=None, currency=None):
        """
        Returns the account balance of a user for a particular token
        :param request_id: the request ID. Will be returned as part of the response
        :param currency: the currency, optional
        :return: response, below format,
        {
            "id": 11,
            "method": "private/get-account-summary",
            "code": 0,
            "result": {
                "accounts": [
                    {
                        "balance": 99999999.905000000000000000,
                        "available": 99999996.905000000000000000,
                        "order": 3.000000000000000000,
                        "stake": 0,
                        "currency": "CRO"
                    }
                ]
            }
        }
        """
        params = {'currency': currency} if currency else dict()
        return self._post('get-account-summary', request_id, params)

    def create_market_sell_order(self, instrument_name, quantity, request_id=None, client_order_id=None):
        """
        Creates a market sell order for the given instrument name
        :param instrument_name: the instrument name
        :param quantity: the quantity to be sold
        :param request_id: the request id, optional
        :param client_order_id: the client order id, optional
        :return: response with below format,
        {
            "id": 11,
            "method": "private/create-order",
            "result": {
                "order_id": "337843775021233500",
                "client_oid": "my_order_0002"
            }
        }
        """
        params = {
            'instrument_name': instrument_name,
            'side': 'SELL',
            'type': 'MARKET',
            'quantity': quantity,
        }
        params.update({'client_oid': client_order_id} if client_order_id else dict())
        return self._post('create-order', request_id, params)

    def create_limit_sell_order(self, instrument_name, quantity, price, request_id=None, client_order_id=None):
        """
        Creates a limit sell order for the given instrument name
        :param instrument_name: the instrument name
        :param quantity: the quantity to be sold
        :param price: the price at which you want to sell
        :param request_id: the request id, optional
        :param client_order_id: the client order id, optional
        :return: response with below format,
        {
            "id": 11,
            "method": "private/create-order",
            "result": {
                "order_id": "337843775021233500",
                "client_oid": "my_order_0002"
            }
        }
        """
        params = {
            'instrument_name': instrument_name,
            'price': price,
            'side': 'SELL',
            'type': 'LIMIT',
            'quantity': quantity,
        }
        params.update({'client_oid': client_order_id} if client_order_id else dict())
        return self._post('create-order', request_id, params)

    def create_market_buy_order(self, instrument_name, notional, request_id=None, client_order_id=None):
        """
        Creates a market buy order for the given instrument name
        :param instrument_name: the instrument name
        :param notional: the notional amount to be spent
        :param request_id: the request id, optional
        :param client_order_id: the client order id, optional
        :return: response with below format,
        {
            "id": 11,
            "method": "private/create-order",
            "result": {
                "order_id": "337843775021233500",
                "client_oid": "my_order_0002"
            }
        }
        """
        params = {
            'instrument_name': instrument_name,
            'side': 'BUY',
            'type': 'MARKET',
            'notional': notional,
        }
        params.update({'client_oid': client_order_id} if client_order_id else dict())
        return self._post('create-order', request_id, params)

    def create_limit_buy_order(self, instrument_name, quantity, price, request_id=None, client_order_id=None):
        """
        Creates a limit sell order for the given instrument name
        :param instrument_name: the instrument name
        :param quantity: the quantity to be sold
        :param price: the price at which you want to buy
        :param request_id: the request id, optional
        :param client_order_id: the client order id, optional
        :return: response with below format,
        {
            "id": 11,
            "method": "private/create-order",
            "result": {
                "order_id": "337843775021233500",
                "client_oid": "my_order_0002"
            }
        }
        """
        params = {
            'instrument_name': instrument_name,
            'price': price,
            'side': 'BUY',
            'type': 'LIMIT',
            'quantity': quantity,
        }
        params.update({'client_oid': client_order_id} if client_order_id else dict())
        return self._post('create-order', request_id, params)

    def cancel_order(self, instrument_name, order_id, request_id=None):
        """
        Cancels the open order for the given instrument name
        :param instrument_name: the instrument name
        :param order_id: the order id to be cancelled
        :param request_id: the request id to be returned in response, optional
        :return: response of below format,
        {
          "id": 11,
          "method": "private/cancel-order",
          "code":0
        }
        """
        params = {
            "instrument_name": instrument_name,
            "order_id": order_id,
        }
        return self._post('cancel-order', request_id, params)

    def cancel_all_orders(self, instrument_name, request_id=None):
        """
        Cancels all open orders for the given instrument name
        :param instrument_name: the instrument name
        :param request_id: the request id to be returned in response, optional
        :return: response of below format,
        {
          "id": 11,
          "method": "private/cancel-all-orders",
          "code":0
        }
        """
        params = {"instrument_name": instrument_name}
        return self._post('cancel-all-orders', request_id, params)

    def get_order_history(self, instrument_name=None, request_id=None, page=0, page_size=20):
        """
        Gets the order history for the account for the last 24 hours
        :param instrument_name: the instrument name for which we want the order history
        :param request_id: the request id to be returned in response, optional
        :param page: the page number, defaults to 0
        :param page_size: the page size, defaults to 20, max value 200
        :return: response format as below,
        {
          "id": 11,
          "method": "private/get-order-history",
          "code": 0,
          "result": {
            "order_list": [
              {
                "status": "FILLED",
                "side": "SELL",
                "price": 1,
                "quantity": 1,
                "order_id": "367107623521528457",
                "client_oid": "my_order_0002",
                "create_time": 1588777459755,
                "update_time": 1588777460700,
                "type": "LIMIT",
                "instrument_name": "ETH_CRO",
                "cumulative_quantity": 1,
                "cumulative_value": 1,
                "avg_price": 1,
                "fee_currency": "CRO"
              },
            ]
          }
        }
        """
        params = {'page': page, 'page_size': page_size}
        params.update({'instrument_name': instrument_name} if instrument_name else dict())
        return self._post('get-order-history', request_id, params)

    def get_open_order(self, instrument_name=None, request_id=None, page=0, page_size=20):
        """
        Gets all open orders for a particular instrument
        :param instrument_name: the instrument name
        :param request_id: the request id to be returned in response, optional
        :param page: the page number, defaults to 0
        :param page_size: the page size, defaults to 20
        :return: response with format as follows,
        {
          "id": 11,
          "method": "private/get-open-orders",
          "code": 0,
          "result": {
            "count": 1177,
            "order_list": [
              {
                "status": "ACTIVE",
                "side": "BUY",
                "price": 1,
                "quantity": 1,
                "order_id": "366543374673423753",
                "client_oid": "my_order_0002",
                "create_time": 1588760643829,
                "update_time": 1588760644292,
                "type": "LIMIT",
                "instrument_name": "ETH_CRO",
                "cumulative_quantity": 0,
                "cumulative_value": 0,
                "avg_price": 0,
                "fee_currency": "CRO"
              },
            ],
          }
        }
        """
        params = {'page': page, 'page_size': page_size}
        params.update({'instrument_name': instrument_name} if instrument_name else dict())
        return self._post('get-open-orders', request_id, params)

    def get_order_detail(self, order_id, request_id=None):
        """
        Gets details on a particular order ID
        :param order_id: the order id
        :param request_id: the request id to be returned in response, optional
        :return: response of below format,
        {
          "id": 11,
          "method": "private/get-order-detail",
          "code": 0,
          "result": {
            "trade_list": [
              {
                "side": "BUY",
                "instrument_name": "ETH_CRO",
                "fee": 0.007,
                "trade_id": "371303044218155296",
                "create_time": 1588902493045,
                "traded_price": 7,
                "traded_quantity": 7,
                "fee_currency": "CRO",
                "order_id": "371302913889488619"
              }
            ],
            "order_info": {
              "status": "FILLED",
              "side": "BUY",
              "order_id": "371302913889488619",
              "client_oid": "9_yMYJDNEeqHxLqtD_2j3g",
              "create_time": 1588902489144,
              "update_time": 1588902493024,
              "type": "LIMIT",
              "instrument_name": "ETH_CRO",
              "cumulative_quantity": 7,
              "cumulative_value": 7,
              "avg_price": 7,
              "fee_currency": "CRO"
            }
          }
        }
        """
        params = {'order_id': order_id}
        return self._post('get-order-detail', request_id, params)

    def get_trades(self, instrument_name=None, request_id=None, page=0, page_size=20):
        """
        Gets all executed trades for a particular instrument in the last 24 hours
        :param instrument_name: the instrument name
        :param request_id: the request id to be returned in response, optional
        :param page: the page number, defaults to 0
        :param page_size: the page size, defaults to 20
        :return: response with format as follows,
        {
          "id": 11,
          "method": "private/get-trades",
          "code": 0,
          "result": {
            "trade_list": [
              {
                "side": "SELL",
                "instrument_name": "ETH_CRO",
                "fee": 0.014,
                "trade_id": "367107655537806900",
                "create_time": 1588777459755,
                "traded_price": 7,
                "traded_quantity": 1,
                "fee_currency": "CRO",
                "order_id": "367107623521528450"
              }
            ]
          }
        }
        """
        params = {'page': page, 'page_size': page_size}
        params.update({'instrument_name': instrument_name} if instrument_name else dict())
        return self._post('get-trades', request_id, params)

    def _post(self, sub_url, request_id, params):
        method_name = urljoin('private/', sub_url)
        url = urljoin(self._private_url, sub_url)
        request_body = PrivateAPIClient._get_request_body(method_name, params, req_id=request_id)
        debug(request_body)
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(request_body)
        )
        return response.json()

    @staticmethod
    def _get_request_body(method, params, req_id=None):
        req_id = req_id or int(time.time())
        api_key = os.environ.get('CRO_API_KEY')
        nonce = int(time.time() * 1000)
        params = params or dict()
        sig = PrivateAPIClient._get_digital_signature(method, api_key, nonce, req_id=req_id, params=params)
        return {
            'api_key': api_key,
            'id': req_id,
            'method': method,
            'nonce': nonce,
            'params': params,
            'sig': sig,
        }

    @staticmethod
    def _get_digital_signature(method, api_key, nonce, req_id=None, params=None):
        params_str = ''
        for key in sorted(set(params or dict())):
            params_str = f'{params_str}{key}{params[key]}'
        secret_key = os.environ.get('CRO_SECRET_KEY')
        sig_payload = f"{method}{req_id or ''}{api_key}{params_str}{nonce}"
        sig = hmac.new(
            bytes(str(secret_key), 'utf-8'),
            msg=bytes(sig_payload, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return sig


if __name__ == '__main__':
    logging.basicConfig(level=DEBUG)
    private = PrivateAPIClient(is_sandbox=False)
    summary = private.get_account_summary(currency='CRO')
    print(summary)
    # sell_market = private.create_market_sell_order('CRO_USDT', 1)
    # print(sell_market)
    # buy_market = private.create_market_buy_order('CRO_USDT', 0.017)
    # print(buy_market)
    # sell_limit = private.create_limit_sell_order('CRO_USDT', 1, 0.20)
    # print(sell_limit)
    # buy_limit = private.create_limit_buy_order('CRO_USDT', 1, 0.015)
    # print(buy_limit)
    # cancel_response = private.cancel_order('CRO_USDT', '666555844043257698')
    # print(cancel_response)
    # cancel_all = private.cancel_all_orders('CRO_USDT')
    # print(cancel_all)
    # order_hist = private.get_order_history()
    # print(order_hist)
    # open_order = private.get_open_order('CRO_USDT')
    # print(open_order)
    # order_details = private.get_order_detail('666555808464096675')
    # print(order_details)
    # trades = private.get_trades()
    # print(trades)
