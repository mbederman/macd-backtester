import backtrader as bt
import math

class MACDStrategy(bt.Strategy):
    def __init__(self):
        self.macd = bt.indicators.MACD(self.data.close, plotname="MACD")

        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        self.sma = bt.indicators.SMA(self.data.close, period=50, plotname="50 day moving average")

        self.size = 0

    def next(self):
        if self.position.size == 0 and self.data.close > self.sma:
            if self.crossover > 0:
                amt_to_invest = (.95 * self.broker.cash)
                self.size = math.floor(amt_to_invest / self.data.close)

                order = self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                self.sell(size=self.size)

    def notify_order(self, order):
        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                print(f"Buy {self.size} shares at {order.executed.price}")
            else:  # Sell
                print(f"Sell {self.size} shares at {order.executed.price}")
        # Sentinel to None: new orders allowed
        self.order = None

class MACDStrategy2(bt.Strategy):
    def __init__(self):
        self.macd = bt.indicators.MACD(self.data.close, plotname="MACD")

        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        self.sma = bt.indicators.SMA(self.data.close, period=50, plotname="50 day moving average")

        self.size = 0

        self.executed_price = 0

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amt_to_invest = (.95 * self.broker.cash)
                self.size = math.floor(amt_to_invest / self.data.close)

                self.buy(size=self.size)

        if self.position.size > 0:
            if self.data.close > (1.02 * self.executed_price):
                self.sell(size=self.size)

    def notify_order(self, order):
        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                print(f"Buy {self.size} shares at {order.executed.price}")
                self.executed_price = order.executed.price
            else:  # Sell
                print(f"Sell {self.size} shares at {order.executed.price}")
                self.executed_price = 0
        # Sentinel to None: new orders allowed
        self.order = None

