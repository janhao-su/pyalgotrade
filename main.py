# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pyalgotrade import plotter
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.tools import yahoofinance
import pyalgotrade
import sma_crossover
import macd
import talib
from pyalgotrade.stratanalyzer import sharpe
import rsi
import bban
import diff
import feed_twgrs

entrySMA = 200
exitSMA = 5
rsiPeriod = 2
overBoughtThreshold = 90
overSoldThreshold = 10


instrument = "3034.TW"#"2330.TW"
#instrument = "2330.TW"
instrument = "2618.TW"
instruments = [instrument]
# Load the yahoo feed from the CSV file
#feed = yahoofeed.Feed()
#feed.addBarsFromCSV("2330.TW", "dia-2015.csv")
#feed = yahoofinance.build_feed([instructment], 2015,2016,"." )
feed = feed_twgrs.build_feed(instruments, 2015,2016,".")
#myStrategy = macd.macd_strategy(feed, "3034.TW")
#feed = yahoofinance.build_feed(["2330.TW"], 2015,2016,"." )

#myStrategy = macd.macd_strategy(feed, instructment)
myStrategy = diff.macd_strategy(feed, instrument)
#myStrategy = rsi.RSI2(feed, "2330.TW",entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
#myStrategy = rsi.RSI2(feed,instructment,entrySMA, exitSMA, rsiPeriod, overBoughtThreshold, overSoldThreshold)
# Evaluate the strategy with the feed's bars.
#myStrategy = sma_crossover.SMACrossOver(feed, instructment, 20)
#myStrategy = bban.BBands(feed,instructment, 40)
#

#myStrategy = sma_crossover.SMACrossOver(feed, "2330.TW", 20)

# Attach a returns analyzers to the strategy.
returnsAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(returnsAnalyzer)
sharpeRatioAnalyzer = sharpe.SharpeRatio()
myStrategy.attachAnalyzer(sharpeRatioAnalyzer)

# Attach the plotter to the strategy.
plt = plotter.StrategyPlotter(myStrategy)
# Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
#plt.getInstrumentSubplot("3034.TW").addDataSeries("SMA", myStrategy.getSMA())
plt.getInstrumentSubplot(instrument).addDataSeries("SMA", myStrategy.getSMA())
# Plot the simple returns on each bar.
#plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
plt.getOrCreateSubplot(instrument).addDataSeries("MACD-HIST", myStrategy.gethist())
plt.getOrCreateSubplot(instrument).addDataSeries("MACD-signal", myStrategy.getsignal())
plt.getOrCreateSubplot(instrument).addDataSeries("MACD", myStrategy.getmacd())
#plt.getOrCreateSubplot("vol").addDataSeries("Vol",  myStrategy.getVol())
#plt.getOrCreateSubplot("diff").addDataSeries("diff",  myStrategy.getdiff())
plt.getOrCreateSubplot("diff").addDataSeries("diffsma",  myStrategy.getdiffsma())
plt.getOrCreateSubplot("diff").addDataSeries("diffsma2",  myStrategy.getdiffsma2())

#plt.getInstrumentSubplot(instructment).addDataSeries("upper", myStrategy.getBollingerBands().getUpperBand())
#plt.getInstrumentSubplot(instructment).addDataSeries("middle", myStrategy.getBollingerBands().getMiddleBand())
#plt.getInstrumentSubplot(instructment).addDataSeries("lower", myStrategy.getBollingerBands().getLowerBand())

# Run the strategy.
myStrategy.run()
myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)
# Plot the strategy.
from matplotlib.widgets import Cursor
#cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
#print  plt.figure().axes#
plt.plot()
