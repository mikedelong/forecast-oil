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
from pandas import read_excel
from pandas import to_datetime
from pandas.plotting import register_matplotlib_converters
from seaborn import lineplot
from pandas import DataFrame
from matplotlib.pyplot import show

if __name__ == '__main__':
    time_start = time()
    register_matplotlib_converters()
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
    df = read_excel(io=url, names=['date', 'value'], sheet_name=sheet_name, skiprows=2, )
    df['date'] = df['date'].apply(to_datetime)
    logger.info(df.shape)
    model = Prophet()
    model.fit(df=df.rename(columns={'date': 'ds', 'value': 'y'}, ))
    ax = lineplot(x='date', y='value', data=df)

    # roll up the projection dates from the max date a week at a time
    start_date = df['date'].max()
    logger.info(start_date)
    dates_df = DataFrame([start_date + datetime.timedelta(weeks=current) for current in range(1, 520)], columns=['ds'])
    prediction_df = model.predict(df=dates_df)
    model.plot(fcst=prediction_df, uncertainty=True, ax=ax, plot_cap=True, xlabel='ds', ylabel='y', )
    show()

    logger.info('total time: {:5.2f}s'.format(time() - time_start))
