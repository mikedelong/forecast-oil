import datetime
from logging import FileHandler
from logging import INFO
from logging import StreamHandler
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from sys import stdout
from time import time

from fbprophet import Prophet
from pandas import read_csv
from pandas.plotting import register_matplotlib_converters

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
    # input_file = './data/DP_LIVE_19102020150254641.csv'
    # input_file = './data/DP_LIVE_09112020172606257.csv'
    input_file = './data/DP_LIVE_23112020174032843.csv'
    # todo check for existence before trying to read the CSV file
    df = read_csv(filepath_or_buffer=input_file)
    logger.info(df.shape)
    logger.info(df['LOCATION'].value_counts().to_dict())
    logger.info('we have {} unique locations'.format(df['LOCATION'].nunique()))
    for column in ['Flag Codes', 'INDICATOR']:
        logger.info('{} values are {}'.format(column, df[column].unique().tolist()))
    locations = sorted(df['LOCATION'].unique(), reverse=False, )
    # todo need to handle these differently because they are aggregates
    excluded_locations = {'EU28', 'G20', 'OECD', 'WLD'}
    locations = [location for location in locations if location not in excluded_locations]
    for location in locations:
        sample_df = df[df['LOCATION'] == location].dropna(subset=['Value']).drop(columns=['Flag Codes'])
        sample_df = sample_df.sort_values(ascending=True, axis=0, by='TIME', )
        logger.info('{}: {} {}'.format(location, len(sample_df), sample_df['TIME'].max()))
    world_df = df[df['LOCATION'] == 'WLD'].dropna(subset=['Value']).drop(columns=['Flag Codes'])
    model = Prophet()
    model.fit(df=world_df[['TIME', 'Value']].rename(columns={'TIME': 'ds', 'Value': 'y'}, ))
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    logger.info('total time: {:5.2f}s'.format(time() - time_start))
