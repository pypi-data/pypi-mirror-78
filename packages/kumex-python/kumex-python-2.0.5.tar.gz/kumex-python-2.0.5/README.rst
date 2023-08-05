===============================
Welcome to kumex-python-sdk
===============================

.. image:: https://img.shields.io/pypi/l/python-kumex.svg
    :target: https://github.com/Kucoin/kumex-python-sdk/blob/master/LICENSE

.. image:: https://img.shields.io/badge/python-3.6%2B-green
    :target: https://pypi.org/project/python-kumex


Features
--------

- Implementation of REST endpoints
- Simple handling of authentication
- Response exception handling
- Implement websockets (note only python3.6+)


Quick Start
-----------

Register an account with `KuMEX <https://futures.kucoin.com//ucenter/signup>`_.

To test on the Sandbox  with `KuMEX Sandbox <https://sandbox-futures.kucoin.com>`_.

`Generate an API Key <https://futures.kucoin.com/api/create>`_
or `Generate an API Key in Sandbox <https://sandbox-futures.kucoin.com/account/api>`_ and enable it.

.. code:: bash

    pip install kumex-python

.. code:: python

    #  MarketData
    from kumex.client import Market
    client = Market(url='https://api-futures.kucoin.com')
    # client = Market()
    # or connect to Sandbox
    # client = Market(url='https://api-sandbox-futures.kucoin.com')
    # client = Market(is_sandbox=True)

    # get l3_order_book
    l3_depth = client.l3_order_book('XBTUSDM')

    # get l2_order_book
    l2_depth = client.l2_order_book('XBTUSDM')

    # get symbol ticker
    klines = client.get_ticker("XBTUSDM")

    # get symbol ticker
    server_time = client.get_server_timestamp()

    api_key = '<api_key>'
    api_secret = '<api_secret>'
    api_passphrase = '<api_passphrase>'

    # Trade
    from kumex.client import Trade
    client = Trade(api_key, api_secret, api_passphrase)

    # or connect to Sandbox
    # client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)

    # place a limit buy order
    order_id = client.create_limit_order('XBTUSDM', 'buy', '1', '30', '8600')

    # place a market buy order   Use cautiously
    order_id = client.create_market_order('XBTUSDM', 'buy', '1')

    # cancel limit order 
    client.cancel_order('5bd6e9286d99522a52e458de')

    # cancel all limit order 
    client.cancel_all_limit_order('XBTUSDM')

    # User
    from kumex.client import User
    client = User(api_key, api_secret, api_passphrase)

    # or connect to Sandbox
    # client = User(api_key, api_secret, api_passphrase, is_sandbox=True)

    address = client.get_withdrawal_quota('XBT')

Websockets
----------

.. code:: python

    import asyncio
    from kumex.client import WsToken
    from kumex.ws_client import KumexWsClient


    async def main():
        async def deal_msg(msg):
            if msg['topic'] == '/contractMarket/level2:XBTUSDM':
                print(f'Get XBTUSDM Ticker:{msg["data"]}')
            elif msg['topic'] == '/contractMarket/level3:XBTUSDTM':
                print(f'Get XBTUSDTM level3:{msg["data"]}')

        # is public
        # client = WsToken()
        # is private
        client = WsToken(url='https://api-futures.kucoin.com', key='', secret='', passphrase='')
        # is sandbox
        # client = WsToken('https://api-sandbox-futures.kucoin.com/')
        # client = WsToken(is_sandbox=True)
        ws_client = await KumexWsClient.create(loop, client, deal_msg, private=False)
        await ws_client.subscribe('/contractMarket/level2:XBTUSDM')
        await ws_client.subscribe('/contractMarket/level3:XBTUSDM')
        while True:
            await asyncio.sleep(60, loop=loop)


    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
