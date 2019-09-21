import matplotlib.pyplot as plt
import pandas as pd
from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.market import Market
import time
import logging


def setup_bitshares_market(bts_symbol):
    bitshares_instance = BitShares(
        "wss://losangeles.us.api.bitshares.org/ws",
        nobroadcast=True  # <<--- set this to False when you want to fire!
    )
    set_shared_bitshares_instance(bitshares_instance)
    bts_market = Market(
        bts_symbol,
        bitshares_instance=bitshares_instance
    )
    return bts_market


def plot_orderbook(ob_df, invert: bool, barwidth: float):
    # get order book and visualize quickly with matplotlib.
    plt.style.use('ggplot')
    bwidth = barwidth
    if bwidth is None:
        bwidth = 0.1

    ob_df['colors'] = 'g'
    ob_df.loc[ob_df.type == 'asks', 'colors'] = 'r'

    # for use with python 3.6.8
    price = ob_df.price.to_numpy()
    vol = ob_df.vol.to_numpy()
    invert_price = ob_df.invert.to_numpy()  # use if needed

    plot_price = price
    if invert is True:
        plot_price = invert_price

    plt.bar(price, vol, bwidth, color=ob_df.colors, align='center')
    # use below line if python 3.7, error with python 3.6.8
    # plt.bar(ob_df.price, ob_df.vol, color=ob_df.colors)


def plot_df(df, title: str, symbol: str, invert: bool, bar_width: float):
    plt.clf()
    plot_orderbook(df, invert=invert, barwidth=bar_width)
    plt.title(title + ":"+ symbol)
    plt.ylabel('volume')
    plt.xlabel('price')
    plt.tight_layout()


def get_bts_orderbook_df(ob, type, inversion: bool):
    price_vol = list()
    if inversion:
        for i in range(len(ob[type])):
            price = ob[type][i]['price']
            invert_price = 1/price
            vol = ob[type][i]['quote']
            vol2 = ob[type][i]['base']  # is this the actual volume?
            price_vol.append([price, vol['amount'], vol2['amount'], invert_price])

        df = pd.DataFrame(price_vol)
        df.columns = ['price', 'vol', 'vol_base', 'invert']
    else:
        for i in range(len(ob[type])):
            price = ob[type][i]['price']
            invert_price = 1/price
            vol = ob[type][i]['quote']
            price_vol.append([price, vol['amount'], invert_price])
        df = pd.DataFrame(price_vol)
        df.columns = ['price', 'vol', 'invert']

    df['timestamp'] = int(time.time())
    df['type'] = type
    return df


def get_ob_data(bts_market, depth: int, invert: bool):
    # get bitshares order book for current market
    bts_orderbook = bts_market.orderbook(limit=depth)
    ask_df = get_bts_orderbook_df(bts_orderbook, 'asks', invert)
    bid_df = get_bts_orderbook_df(bts_orderbook, 'bids', invert)
    bts_df = pd.concat([ask_df, bid_df])
    bts_df.sort_values('price', inplace=True, ascending=False)
    return bts_df


if __name__ == '__main__':
    title = "Bitshares DEX"
    bts_symbol = "OPEN.BTC/USD"
    depth = 10
    poll_time = 3 # time to wait before polling again
    bar_width = 30
    invert = False

    bts_market = setup_bitshares_market(bts_symbol)
    log = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    while True:
        try:
            plt.ion() # interactive plot
            bts_df = get_ob_data(bts_market, depth, invert)
            log.info(f'{title} {bts_symbol}:\n {bts_df}')
            plot_df(bts_df, title, bts_symbol, invert, bar_width)
            plt.pause(poll_time)
            plt.draw()
        except Exception as e:
            log.error(e)
            break

