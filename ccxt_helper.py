import logging
import os
import configparser
import ccxt
import json

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


def get_exchange_config(config_file):
    try:
        config_dir = os.path.dirname(__file__)
        parser = configparser.ConfigParser()
        parser.read(os.path.join(config_dir, config_file))
        exch_ids = parser.sections()
        log.info("exchange ids")
        log.info(exch_ids)
        sec = {section_name: dict(parser.items(section_name)) for section_name in exch_ids}
        return sec
    except (FileNotFoundError, PermissionError, OSError) as e:
        log.error(e)
        pass


def get_exchange(config_sections):
    # need to fix below in order to check for for acceptable exchanges and parameters
    # for now, get 0th exchange
    exch_name = list(config_sections)[0]
    apikey = config_sections[exch_name]['api_key']
    secret = config_sections[exch_name]['secret']
    log.info(f"API Key:  {apikey}")
    log.info(f"SECRET: {secret})")

    # coin tiger requires an API key, even if only for ticker data
    ccxt_ex = getattr(ccxt, exch_name)({
        "apiKey": apikey,
        "secret": secret,
        'timeout': 30000,
        'enableRateLimit': True,
        'verbose': False,
    })
    return ccxt_ex


def get_ccxt_module():
    config_sections = get_exchange_config()
    log.info(config_sections)
    ccxt_ex = get_exchange(config_sections)
    return ccxt_ex


def write_dict(l2_ob, file_name):
    with open(file_name, 'w') as f:
        s = f.write(json.dumps(l2_ob))


def read_dict(file_name):
    with open(file_name, 'r') as f:
        static_ob = json.loads(f.read())
    return static_ob


