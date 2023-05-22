import csv
import datetime
import pandas as pd
from binance import BinanceSocketManager


def current_full_hour() -> int:
    return int(datetime.datetime.now().strftime("%H"))


async def available_usdt_for_trade(client, pct_of_portfolio_used: float):
    trade_amount = await client.get_asset_balance('USDT') * pct_of_portfolio_used
    return trade_amount


async def current_asset_price(client, security):
    bm = BinanceSocketManager(client)
    ts = bm.trade_socket(security)

    async with ts as tscm:
        res = await tscm.recv()
        price = float(res['p'])

    await client.close_connection()

    return price


def get_list_of_open_trades(client):
    orders = client.get_open_orders()
    open_trades = []
    for order in orders:
        open_trades.append([order['orderId'], order['symbol']])

    return open_trades


def close_all_trades(client):
    """
    format: [tradeId][symbol]
    """

    open_trades = get_list_of_open_trades(client)

    # cancel an order
    for open_trade in open_trades:
        client.cancel_order(symbol=open_trade[1], orderId=open_trade[0])


def write_to_csv(client):
    res = client.get_open_orders()
    with open('open_trades.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["OrderId", "Symbol"])
        for r in res:
            writer.writerow([r['orderId'], r['symbol']])


def delete_from_csv(client):
    open_trades = get_list_of_open_trades(client)   # [123, BTC]
    df = pd.read_csv('open_trades.csv')             # [245, ETH,
                                                    # 123, BTC]

    # iterate through df and open_trades
    # delete if there is open_trade in df but not in open_trades

    # create dict from df
    df_dict = {}
    for index, row in df.iterrows():
        df_dict[row['OrderId']] = row['Symbol']

    print(df_dict)
    print(open_trades)













