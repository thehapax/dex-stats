from ccxt_helper import get_exchange_config, get_exchange, read_dict, write_dict
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# update this to reflect your config file
config_file = "safe/secrets_test.ini"


def get_test_l2ob(symbol):
    config_sections = get_exchange_config(config_file)
    log.info(config_sections)
    ccxt_ex = get_exchange(config_sections)

    log.info(f"Fetch Ticker for {symbol} : {ccxt_ex.fetch_ticker(symbol)}\n")
    #print(ccxt_ex.fetch_free_balance())
    l2_ob = ccxt_ex.fetch_l2_order_book(symbol=symbol, limit=None)
    return l2_ob


if __name__ == '__main__':

    symbol = 'BTC/USDT'
#    symbol = 'BTS/BTC'
    log.info("symbol: {} ".format(symbol))
    l2_ob = get_test_l2ob(symbol)

"""
    file_name = 'cex_ob.txt'
    write_dict(l2_ob, file_name)
    static_ob = read_dict(file_name)
    print(static_ob)
"""
