import pandas as pd
import numpy as np
import pandas_ta as ta


async def get_close_price_dataframe(client: object, security: str, interval: str, total_period: str) -> pd.DataFrame:
    bars = await client.get_historical_klines(security, interval, total_period)

    for line in bars:
        del line[5:]
        del line[0:2]

    df = pd.DataFrame(bars, columns=['high', 'low', 'close'])
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)

    return df


def get_indicator_values(df):
    """
    returns [symbol][indicator][indicatorValue(list)]
    indicatorValue = [previousValue, currentValue]
    """
    names = list(df.columns)

    fast_ma_list = df[names[3]].astype(float)
    slow_ma_list = df[names[4]].astype(float)

    aroon_up_list = df[names[5]].astype(float)
    aroon_down_list = df[names[6]].astype(float)

    return {'fastMA': list(np.around(np.array(fast_ma_list), 2)),
            'slowMA': list(np.around(np.array(slow_ma_list), 2)),
            'aroonUp': list(np.around(np.array(aroon_up_list), 2)),
            'aroonDown': list(np.around(np.array(aroon_down_list), 2))}


def get_sma_price(param, df):
    df.ta.sma(length=param, append=True, column_name='SMA_' + str(param))


def get_aroon_price(param, df):
    df.ta.aroon(length=param, append=True, column_name='AROONU_' + str(param))


async def aroon_sma_strategy(indicators_dict, client, security: str, interval: str, total_period: str):
    df = await get_close_price_dataframe(client, security, interval, total_period)

    get_sma_price(20, df)
    get_sma_price(40, df)
    get_aroon_price(12, df)

    indicators_dict[security] = get_indicator_values(df.tail(2))  # passing last 2 candles

    return indicators_dict
