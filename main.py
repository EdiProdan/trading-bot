import asyncio
from binance import AsyncClient, BinanceSocketManager
from time import sleep
from src import indicators, signals, helpers, orders, strategies
import os
import pprint


async def main():

    client = await AsyncClient.create(api_key=os.environ["BINANCE_TEST_API_KEY"],
                                      api_secret=os.environ["BINANCE_TEST_SECRET"],
                                      testnet=True)
    # client = await AsyncClient.create()

    # pprint.pprint(await client.get_account())
    bm = BinanceSocketManager(client)

    indicators_dict = {}
    indicators_dict = await indicators.aroon_sma_strategy(indicators_dict, client, 'BTCUSDT', '1h', '5 days ago UTC')
    # indicators = await aroon_sma_strategy(indicators, client, 'ETHUSDT', '1h', '5 days ago UTC')
    print(indicators_dict)


    # await strategies.strategy(client, indicators_dict, 'BTCUSDT')
    short_trade = await orders.market_sell_order_with_tp_sl(client, "BTCUSDT", 0.001, 3, 1)
    # # print(long_trade)
    # info = await client.get_exchange_info()
    # # # iterate through info and get all symbols
    # #
    # for symbol in info['symbols']:
    #     print(symbol['allowTrailingStop'])
    #     print(symbol['orderTypes'])
    #     print(symbol['symbol'])
    # # # pprint.pprint(info['symbols'][0]['allowTrailingStop'])

    pprint.pprint(await client.get_open_orders())

    await client.close_connection()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
