
from pyalgotrade import strategy
from pyalgotrade.technical import macd
from pyalgotrade.technical import cross
import numpy as np
import talib
from pyalgotrade.technical import ma
from pyalgotrade import dataseries


class macd_strategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(macd_strategy, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__macd = macd.MACD(feed[instrument].getPriceDataSeries(),12,26,9)
        self.__vol = feed[instrument].getVolumeDataSeries()
        self.__smavol = ma.SMA(self.__vol, 20)
        self.__sma = ma.SMA(self.__prices, 20)
        self.__diffsma = ma.SMA(self.__prices, 5)
        self.short = 0
        self.__diff = dataseries.SequenceDataSeries(None)
        self.__diff2 = dataseries.SequenceDataSeries(None)
        self.__diffsma = dataseries.SequenceDataSeries(None) # ma.SMA(self.__diff, 20)
        self.__diffsma2 = dataseries.SequenceDataSeries(None) # ma.SMA(self.__diff, 20)
        self.__diffsma3 = dataseries.SequenceDataSeries(None) # ma.SMA(self.__diff, 20)
        pass

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def gethist(self):
        return self.__macd.getHistogram()

    def getVol(self):
        return self.__vol

    def getsignal(self):
        return self.__macd.getSignal()

    def getmacd(self):
        return self.__macd

    def getSMA(self):
        return self.__sma

    def getdiff(self):
        return self.__diff

    def getdiffsma(self):
        return self.__diffsma

    def getdiffsma2(self):
        return self.__diffsma2
    def getdiffsma3(self):
        return self.__diffsma3

    def onBars(self, bars):
        close = np.array(self.__prices[:])

        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        #hist = macdhist.tolist()
        hist= self.gethist()
        signal = self.getsignal()
        if len(self.__prices[:]) == 1 :
            self.__diff.appendWithDateTime(self.__prices.getDateTimes()[-1] , 0)
            #self.__diff.appendWithDateTime(self.__sma.getDateTimes()[-1], 0)
            #print 0
        else :
            self.__diff.appendWithDateTime(self.__prices.getDateTimes()[-1], self.__prices[-1]  -  self.__prices[-2])
            #self.__diff.appendWithDateTime(self.__sma.getDateTimes()[-1], self.__prices[-1] - self.__prices[-2])

        if len(self.__prices[:]) <22:
            # self.__diff.appendWithDateTime(self.__prices.getDateTimes()[-1] , 0)
            self.__diff2.appendWithDateTime(self.__sma.getDateTimes()[-1], 0)
            # print 0
        else:
            # self.__diff.appendWithDateTime(self.__prices.getDateTimes()[-1], self.__prices[-1]  -  self.__prices[-2])
            #self.__diff2.appendWithDateTime(self.__sma.getDateTimes()[-1], self.__sma[-1] - self.__sma[-2])
            pass

        if len(self.__prices[:]) < 20:
            self.__diffsma.appendWithDateTime(self.__prices.getDateTimes()[-1], 0 )
        else :
            #self.__diffsma.appendWithDateTime(self.__prices.getDateTimes()[-1], sum(self.__diff[-1:-21:-1])/20)
            self.__diffsma.appendWithDateTime(self.__prices.getDateTimes()[-1], sum(self.__diff[-1:-21:-1]) )

            #print self.__diff[-1:-21:-1]

        if len(self.__prices[:]) < 3:
            self.__diffsma2.appendWithDateTime(self.__prices.getDateTimes()[-1], 0)
            self.__diffsma3.appendWithDateTime(self.__prices.getDateTimes()[-1],  0)
        else:
            self.__diffsma2.appendWithDateTime(self.__prices.getDateTimes()[-1], sum(self.__diff2[-1:-4:-1]) / 3)
            self.__diffsma3.appendWithDateTime(self.__prices.getDateTimes()[-1], sum(self.__diff[-1:-4:-1]) /3 *5)

            # print self.__diff[-1:-21:-1]
        if self.__position is None:
            #if signal[-1] > 0.0 and signal[-2] <= 0.0 and  hist[-1] > 0.0:
            #if self.__macd[-1] > 0.0 and self.__macd[-2] <= 0.0 and hist[-1] > 0.0:
            #if hist[-1] > 0.0 and hist[-2] <= 0.0 :#and  signal[-1] > 0.0:
            if self.short ==0 and   self.__diffsma[-1] > 0 :#and self.__diffsma3[-1] > 0:#and self.__diffsma[-2] < 0: #and self.__sma[-1]>=self.__sma[-2] and self.__sma[-2] != None and
                shares = int(self.getBroker().getCash() / bars[self.__instrument].getPrice())
                shares -= (shares%1000)
                #print shares, self.getBroker().getCash(),bars[self.__instrument].getPrice()
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
                print "buylong "+ str(bars[self.__instrument].getPrice()) +" " +str(self.__prices.getDateTimes()[-1])
                print self.__diffsma[-5:-1]
                print self.__diffsma3[-5:-1]
                print self.__diff[-5:-1]
                self.buy_price  = bars[self.__instrument].getPrice()
            #elif  cross.cross_below(self.__macd.getSignal(),  self.__macd) > 0  and self.short == 1  and self.__diffsma[-1] < 0: #and self.__sma[-1] <=self.__sma[-2] and self.__sma[-2] != None:
            #    shares = int(self.getBroker().getCash() / bars[self.__instrument].getPrice())
               # shares -=1
                # print shares, self.getBroker().getCash(),bars[self.__instrument].getPrice()
                # Enter a buy market order. The order is good till canceled.
             #   self.__position = self.enterShort(self.__instrument, shares, True)
        #elif not self.__position.exitActive() and  hist[-1] < 0.0 and hist[-2] >= 0.0:
        #elif not self.__position.exitActive() and signal[-1] < 0.0 and signal[-2] >= 0.0:
        #elif not self.__position.exitActive() and self.__macd[-1] < 0.0 and self.__macd[-2] >= 0.0:
#        elif not self.__position.exitActive() and hist[-1] - hist[-2] <= 0.0 and self.short == 1 :
 #           print "sell"
 #           self.__position.exitMarket()
       # elif not self.__position.exitActive() and  cross.cross_below(self.__macd.getSignal(), self.__macd) > 0 and self.short ==1:
        #    print "sell"
        #    self.__position.exitMarket()
        #elif not self.__position.exitActive() and self.__diffsma[-1] < 0 and self.__diffsma[-2] >0and self.short == 0:
        #    print "selllong by sma1 " + str(bars[self.__instrument].getPrice()) + " " + str(
        #        self.__prices.getDateTimes()[-1]) + str(bars[self.__instrument].getPrice() - self.buy_price)
        #    self.__position.exitMarket()
        elif not self.__position.exitActive() and self.__diffsma3[-1] < 0 and self.__diffsma3[-2] >0 and self.short == 0:
            if(bars[self.__instrument].getPrice() - self.buy_price ) < 0 :
                print "###############"

            print "selllong by sma3 " +str( bars[self.__instrument].getPrice())+" " +str(self.__prices.getDateTimes()[-1]) + str(bars[self.__instrument].getPrice() - self.buy_price)
            self.__position.exitMarket()
        elif not self.__position.exitActive() and ( bars[self.__instrument].getPrice() < self.buy_price*0.95 ) and self.short == 0:
            print "selllong by reduce 5 " + str(bars[self.__instrument].getPrice()) + " " + str(
                self.__prices.getDateTimes()[-1]) + str(bars[self.__instrument].getPrice() - self.buy_price)
            self.__position.exitMarket()
        #elif not self.__position.exitActive() and self.__diffsma[-1] < -8 and self.short == 0:
         #   print "selllong by because weak sma " + str(bars[self.__instrument].getPrice()) + " " + str(
         #       self.__prices.getDateTimes()[-1]) + str(bars[self.__instrument].getPrice() - self.buy_price)
         #   self.__position.exitMarket()
        pass
        pass
        pass