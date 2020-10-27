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
from pandas import read_csv

if __name__ == '__main__':
    time_start = time()
    register_matplotlib_converters()
    LOG_PATH = Path('./logs/')
    LOG_PATH.mkdir(exist_ok=True)
    log_file = str(LOG_PATH / 'log-{}-{}.log'.format(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'), 'oecd'))
    format_ = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    handlers_ = [FileHandler(log_file, encoding='utf-8', ), StreamHandler(stdout)]
    log_level_ = INFO
    # noinspection PyArgumentList
    basicConfig(datefmt='%m-%d-%Y %H:%M:%S', format=format_, handlers=handlers_, level=log_level_, )
    logger = getLogger(__name__)
    logger.info('started')

    # OECD data from https://data.oecd.org/energy/crude-oil-production.htm
    input_file = './data/DP_LIVE_19102020150254641.csv'
    df = read_csv(filepath_or_buffer=input_file)
    logger.info(df.shape)
    logger.info(df['Flag Codes'].value_counts().to_dict())
    logger.info(df['LOCATION'].value_counts().to_dict())
    logger.info('we have {} unique locations'.format(df['LOCATION'].nunique()))
    locations = sorted(df['LOCATION'].unique(), reverse=False,)
    for location in locations:
        sample_df = df[df['LOCATION'] == location].dropna(subset=['Value']).drop(columns=['Flag Codes'])
        pass
    logger.info('total time: {:5.2f}s'.format(time() - time_start))