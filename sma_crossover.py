# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 00:47:04 2016

@author: housesu
"""

from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(SMACrossOver, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)
        self.__vol = feed[instrument].getVolumeDataSeries()
        self.__smavol = ma.SMA(self.__vol, smaPeriod)
        self.st = 0

    def getSMA(self):
        return self.__sma


    def getVol(self):
        return self.__vol

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0 and self.st == 0 :
                check5sma_avg = 0
                vot = 0
                vot2 = 0
                for x in range(5) :
                    if self.__sma[-x-1] > self.__sma[-x-1-1] :
                        vot+=1
                for x in range(5):
                    if self.__prices[-x - 1] > self.__prices[-x - 1 - 1]:
                        vot2 += 1
                #if self.__sma[-1] > self.__sma[-2] :
                if vot >= 3 and vot2 >=3 and  self.__sma[-1] > self.__sma[-2]: #self.__sma[-1] > check5sma_avg*1.02:
                    vol = self.__vol
                    #if self.__sma[-1] * 0.98 > self.__sma[-2]:
                    if 1: #self.__vol[-1]  < self.__vol[-2]*1.3 :
                        shares = int(self.getBroker().getCash() / bars[self.__instrument].getPrice())
                        # Enter a buy market order. The order is good till canceled.
                        self.__position = self.enterLong(self.__instrument, shares, True)
                        print "buy"
                        print vol.getDateTimes()[-1]
                        print self.__prices[-5:]
                        print self.__sma[-5:]
                        #print vol[-5:]
                        self.buy_price = self.__prices[-1]
                        self.st = 1
                    else :
                        print "-buy"
                        print vol.getDateTimes()[-1]
                        #print vol[-5:]
                        pass
                else :
                    vol = self.__vol
                    print "-2buy"
                    print vol.getDateTimes()[-1]
                    print self.__prices[-5:]
                    print self.__sma[-5:]
                    pass
                        #print self.__vol[-1]
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below( self.__prices,self.__sma) > 0 :
            self.__position.exitMarket()
            self.st = 0
        #elif not self.__position.exitActive() and self.__sma[-1] < self.__sma[-2] and  self.__sma[-2] < self.__sma[-3]and  self.__sma[-3] < self.__sma[-4]:
        #   self.__position.exitMarket()
        elif not self.__position.exitActive() and self.__prices[-1] < self.buy_price*0.95:
            self.__position.exitMarket()
            self.st = 0
