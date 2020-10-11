import datetime
from logging import FileHandler
from logging import INFO
from logging import StreamHandler
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from sys import stdout
from time import time
from pandas import read_excel

if __name__ == '__main__':
    time_start = time()
    LOG_PATH = Path('./logs/')
    LOG_PATH.mkdir(exist_ok=True)
    log_file = str(LOG_PATH / 'log-{}-{}.log'.format(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'),
                                                     'us_production'))
    format_ = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    handlers_ = [FileHandler(log_file, encoding='utf-8', ), StreamHandler(stdout)]
    log_level_ = INFO
    # noinspection PyArgumentList
    basicConfig(datefmt='%m-%d-%Y %H:%M:%S', format=format_, handlers=handlers_, level=log_level_, )
    logger = getLogger(__name__)
    logger.info('started')

    url = 'https://www.eia.gov/dnav/pet/hist_xls/WCRFPUS2w.xls'
    sheet_name = 'Data 1'
    df = read_excel(io=url, sheet_name=sheet_name, skiprows=2, )
    logger.info(df.shape)

    logger.info('total time: {:5.2f}s'.format(time() - time_start))
