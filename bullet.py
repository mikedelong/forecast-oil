import datetime
from logging import FileHandler
from logging import INFO
from logging import StreamHandler
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from sys import stdout
from time import time
from dateutil.relativedelta import relativedelta

if __name__ == '__main__':
    time_start = time()
    LOG_PATH = Path('./logs/')
    LOG_PATH.mkdir(exist_ok=True)
    log_file = str(LOG_PATH / 'log-{}-{}.log'.format(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S'), 'bullet'))
    format_ = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    handlers_ = [FileHandler(log_file, encoding='utf-8', ), StreamHandler(stdout)]
    log_level_ = INFO
    # noinspection PyArgumentList
    basicConfig(datefmt='%m-%d-%Y %H:%M:%S', format=format_, handlers=handlers_, level=log_level_, )
    logger = getLogger(__name__)
    logger.info('started')

    today = datetime.date.today()
    reference_date = datetime.date(day=1, month=4, year=2020, )
    production_per_day = 100.63 * 1e6

    #  1.7297 trillion
    # https://drillers.com/how-much-oil-is-left-in-the-world/
    estimated_reserve = 1.7297 * 1e12

    days_remaining = int(estimated_reserve // production_per_day)
    logger.info(days_remaining)
    projected_date = reference_date + datetime.timedelta(days=days_remaining)
    logger.info(projected_date)
    remaining = relativedelta(dt1=projected_date, dt2=today, )
    logger.info('{} years, {} months, and {} days.'.format(remaining.years, remaining.months, remaining.days, ))

    logger.info('total time: {:5.2f}s'.format(time() - time_start))
