import csv
import grs
import datetime
import time
import os
import datetime

import pyalgotrade.logger
from pyalgotrade import bar
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils

"""
    thie is pyalgotrade help module
"""

def roc_time_to_west_time(roc_time, ):
    time_peace = roc_time.split("/")
    time_peace[0] = str(int(time_peace[0])-105+2016)

    west_time = '-'.join(time_peace)
    return west_time


def get_year(date):
    return date.split("-")[0]


def build_feed(instruments, fromYear, toYear, storage=".", frequency=bar.Frequency.DAY, timezone=None, skipErrors=False):
    """Build and load a :class:`pyalgotrade.barfeed.yahoofeed.Feed` using CSV files downloaded from Yahoo! Finance.
    CSV files are downloaded if they haven't been downloaded before.

    :param instruments: Instrument identifiers.
    :type instruments: list.
    :param fromYear: The first year.
    :type fromYear: int.
    :param toYear: The last year.
    :type toYear: int.
    :param storage: The path were the files will be loaded from, or downloaded to.
    :type storage: string.
    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param skipErrors: True to keep on loading/downloading files in case of errors.
    :type skipErrors: boolean.
    :rtype: :class:`pyalgotrade.barfeed.yahoofeed.Feed`.
    """
    ret = yahoofeed.Feed(frequency, timezone)

    if not os.path.exists(storage):
        os.mkdir(storage)
    print instruments
    #for year in range(fromYear, toYear+1):
    for instrument in instruments:
        twgrs_instrument = instrument.replace(".TW","")
        twgrs = feed_twgrs(twgrs_instrument, twgrs_instrument, fromYear, toYear)
        ret.addBarsFromCSV(instrument, twgrs.get_file())
    return ret

class  feed_twgrs:
    def __init__(self, tw_stock_id,instruments, from_year, to_year, storage="."):
        self.__tw_stock_id = instruments
        self.__from_year = from_year

        self.__to_year = to_year
        self.__storage = storage
        #month_interval +=1ou
        #time.sleep(1)
        month_interval = (int(datetime.datetime.today().strftime("%Y")) - from_year) * 12 + int(datetime.datetime.today().strftime("%m"))

        #print "month interval %d " % month_interval
        file_name = storage+"/tw"+tw_stock_id+"-"+str(from_year)+".csv"
        self.__file = file_name

        self.__stock = grs.Stock(tw_stock_id,month_interval)
        due_year = to_year + 1

        with open(self.__file, 'wb') as csvfile:
            csv_out = csv.writer(csvfile)
            csv_out.writerow(["Date", "Open", "High", "Low", "Close", "Volume", "Adj Close"])

            for x in self.__stock.raw:
                # print x

                x[0] = roc_time_to_west_time(x[0])
                if int(get_year( x[0])) == due_year:
                    print "due year",due_year,x[0]
                    break
                #to do : Adj Close
                west_fmt = [x[0], x[3], x[4], x[5], x[6], str(int(x[1])), x[4]]
                csv_out.writerow(west_fmt)
        pass

    def get_file(self):
        return self.__file


    pass



