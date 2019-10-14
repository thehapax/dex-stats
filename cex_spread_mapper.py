import pandas as pd
from ccxt_helper import get_ccxt_module

"""

"""

# CEX orderbook
symbol = 'BTC/USDT'
depth = 5 # how deep do you want to map your orders
ccxt_ex = get_ccxt_module()
l2_ob = ccxt_ex.fetch_l2_order_book(symbol=symbol, limit=None)
cex_df = get_cex_data(l2_ob, depth=depth)  # dynamic data

