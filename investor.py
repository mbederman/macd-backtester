import pandas as pd
import backtrader as bt
from strategy import *

STARTING_PORTFOLIO_VALUE = 1000000.0

cerebro = bt.Cerebro()
cerebro.broker.setcash(STARTING_PORTFOLIO_VALUE)

prices = pd.read_csv("AMD.csv", index_col="time", parse_dates=True)

feed = bt.feeds.PandasData(dataname=prices)
cerebro.adddata(feed)
cerebro.addstrategy(MACDStrategy2)

cerebro.run()

final_portfolio_value = cerebro.broker.getvalue()
percent_change = ((final_portfolio_value - STARTING_PORTFOLIO_VALUE) / STARTING_PORTFOLIO_VALUE) * 100
print(f"Percent Change: {percent_change}%")

cerebro.plot()



