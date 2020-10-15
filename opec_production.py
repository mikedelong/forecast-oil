import datetime
from logging import FileHandler
from logging import INFO
from logging import StreamHandler
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from sys import stdout
from time import time

from pandas.plotting import register_matplotlib_converters
from json import load
from urllib.request import urlopen
from json import loads

if __name__ == '__main__':
    time_start = time()
    register_matplotlib_converters()
    LOG_PATH = Path('./logs/')
    LOG_PATH.mkdir(exist_ok=True)
    log_file = str(LOG_PATH / 'log-{}-{}.log'.format(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'),
                                                     'opec_production'))
    format_ = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    handlers_ = [FileHandler(log_file, encoding='utf-8', ), StreamHandler(stdout)]
    log_level_ = INFO
    # noinspection PyArgumentList
    basicConfig(datefmt='%m-%d-%Y %H:%M:%S', format=format_, handlers=handlers_, level=log_level_, )
    logger = getLogger(__name__)
    logger.info('started')

    with open(encoding='ascii', file='settings.json', mode='r', ) as settings_fp:
        settings = load(fp=settings_fp, )
    api_key = settings['api_key']

    url = 'http://api.eia.gov/series/?api_key={}&series_id=STEO.COPR_OPEC.A'.format(api_key)

    with urlopen(url=url, ) as input_fp:
        data = input_fp.read().decode('utf-8')

    data = loads(data)
    data_request = data['request']
    logger.info('total time: {:5.2f}s'.format(time() - time_start))
