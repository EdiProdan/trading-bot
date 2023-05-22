from src import helpers, orders, signals
from time import sleep


async def strategy(client, indicators_dict: dict, security):
    # orders.close_all_trades(client)
    last_full_hour = helpers.current_full_hour()

    while True:

        if signals.long_signal_aroon_ma(indicators_dict, security):
            price = await helpers.current_asset_price(client, security)
            trade_amount = await helpers.available_usdt_for_trade(client, 0.01)
            quantity = trade_amount / price
            long_trades = await orders.market_buy_order_with_tp_sl(client, security, quantity, 0.03, 0.01)
            # helpers.write_to_csv(client)

        elif signals.short_signal_aroon_ma(indicators_dict, security):
            price = await helpers.current_asset_price(client, security)
            trade_amount = await helpers.available_usdt_for_trade(client, 0.01)
            quantity = trade_amount / price
            short_trades = await orders.market_sell_order_with_tp_sl(client, security, quantity, 0.03, 0.01)
            # helpers.write_to_csv(client)

        while helpers.current_full_hour() == last_full_hour:
            sleep(1)
            print("snoozin' innit")
            # remove_from_txt()
        last_full_hour = helpers.current_full_hour()
