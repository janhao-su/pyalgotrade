from grs import Stock
import feed_twgrs as twgrs

import csv

#stock = Stock('2618',12)
#print stock.moving_average(5)
#check =  stock.raw

from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.tools import yahoofinance
from pyalgotrade import plotter
import feed_twgrs

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__vol = feed[instrument].getVolumeDataSeries()
        self.__close = feed[instrument].getCloseDataSeries()

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())
        print self.__close[:]

    def onVol(self, bars):
        self.__vol

    def get_close(self):
        self.__close


# Load the yahoo feed from the CSV file
instrument = "2618.TW"
instruments = [instrument,"2330.TW"]
feed2 = feed_twgrs.build_feed(instruments, 2015,2016,".")
#feed2 = yahoofinance.build_feed([instrument], 2015,2016,".")
#instrument = "2618"
#f_twgrs = twgrs.feed_twgrs(instrument,instrument,2015,2015)
#feed = yahoofeed.Feed()
#feed.addBarsFromCSV(instrument, f_twgrs.get_file())
#myStrategy = MyStrategy(feed, instrument)
myStrategy = MyStrategy(feed2, instrument)
# Evaluate the strategy with the feed's bars.
plt = plotter.StrategyPlotter(myStrategy)
#plt.getOrCreateSubplot("close").addDataSeries("close", myStrategy.get_close())

plt.getOrCreateSubplot("eee").addDataSeries("sma", feed2[instrument].getCloseDataSeries())
myStrategy.run()

myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())



# Plot the strategy.
plt.plot()