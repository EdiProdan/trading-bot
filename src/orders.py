import pprint

from binance.enums import *
import pandas as pd


async def tp_sl_oco_order(market_order, client, security, side, quantity,
                          stop_loss_percentage, take_profit_percentage):
    """
    :param market_order: market order whose fill price dictates TP and SL
    :param client: client
    :param security: asset pair
    :param side: SIDE_BUY or SIDE_SELL, enum
    :param quantity: amount of the asset bought (eg 0.001 BTC)
    :param stop_loss_percentage: positive number between 1 and 100
    :param take_profit_percentage: positive number between 1 and 100
    :return: OCO order details
    """

    if side == SIDE_BUY:
        stop_loss_percentage *= -1
        take_profit_percentage *= -1

    print(security)
    stop_price = round(float(market_order['fills'][0]['price']) * (1 - (stop_loss_percentage / 100)), 2)
    price = round(float(market_order['fills'][0]['price']) * (1 + (take_profit_percentage / 100)), 2)

    oco_order = await client.create_oco_order(symbol=security,
                                              side=side,
                                              quantity=quantity,
                                              stopLimitPrice=stop_price,
                                              stopLimitTimeInForce=TIME_IN_FORCE_GTC,
                                              stopPrice=stop_price,
                                              price=price)
    return oco_order


async def market_buy_order_with_tp_sl(client, security: str, quantity: float, take_profit_percentage: float,
                                      stop_loss_percentage: float):
    market_order = await client.order_market_buy(symbol=security, quantity=quantity)
    print(market_order)
    oco_order = await tp_sl_oco_order(market_order, client, security, SIDE_SELL, quantity,
                                      stop_loss_percentage, take_profit_percentage)
    pprint.pprint(oco_order)

    return [market_order, oco_order]


async def market_sell_order_with_tp_sl(client, security: str, quantity: float, take_profit_percentage: float,
                                       stop_loss_percentage: float):
    market_order = await client.order_market_buy(symbol=security, quantity=quantity)
    print(market_order)
    oco_order = await tp_sl_oco_order(market_order, client, security, SIDE_BUY, quantity,
                                      stop_loss_percentage, take_profit_percentage)
    print(oco_order)

    return [market_order, oco_order]
