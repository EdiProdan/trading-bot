def aroon_long(indicators_dict, security):
    """
    Bullish AROON cross
    """
    return True if (indicators_dict[security]['aroonUp'][-1] >= indicators_dict[security]['aroonDown'][-1] and
                    indicators_dict[security]['aroonUp'][0] <= indicators_dict[security]['aroonDown'][0]) else False


def aroon_short(indicators_dict, security):
    """
    Bearish AROON cross
    """
    return True if (indicators_dict[security]['aroonUp'][-1] <= indicators_dict[security]['aroonDown'][-1] and
                    indicators_dict[security]['aroonUp'][0] >= indicators_dict[security]['aroonDown'][0]) else False


def ma_long(indicators_dict, security):
    """
    Bullish MA cross
    """
    return True if (indicators_dict[security]['fastMA'][-1] >= indicators_dict[security]['slowMA'][-1] and
                    indicators_dict[security]['fastMA'][0] <= indicators_dict[security]['slowMA'][0]) else False


def ma_short(indicators_dict, security):
    """
    Bearish MA cross
    """
    return True if (indicators_dict[security]['fastMA'][-1] <= indicators_dict[security]['slowMA'][-1] and
                    indicators_dict[security]['fastMA'][0] >= indicators_dict[security]['slowMA'][0]) else False


def long_signal_aroon_ma(indicators_dict, security):
    """
    Checks if the signal is given by the cross and if the other indicator is in the setup for an uptrend
    """
    return True if ((aroon_long(indicators_dict, security) and
                     indicators_dict[security]['fastMA'][-1] >= indicators_dict[security]['slowMA'][-1]) or
                    (ma_long(indicators_dict, security) and
                     indicators_dict[security]['aroonUp'][-1] >= indicators_dict[security]['aroonDown'][-1])) else False


def short_signal_aroon_ma(indicators_dict, security):
    """
    Checks if the signal is given by the cross and if the other indicator is in the setup for a downtrend
    """
    return True if ((aroon_short(indicators_dict, security) and
                     indicators_dict[security]['fastMA'][-1] <= indicators_dict[security]['slowMA'][-1]) or
                    (ma_short(indicators_dict, security) and
                     indicators_dict[security]['aroonUp'][-1] <= indicators_dict[security]['aroonDown'][-1])) else False
