import pandas as pd
import numpy
import yfinance as yf
import statistics
# import csv
# pip install pandas
# pip install numpy
# pip install yfinance

# ---------------------------------------------------------------------------------------

# other method for r squared
# from sklearn.linear_model import LinearRegression
# pip install scipy
# pip install scikit-learn

# for charts
import pendulum
import matplotlib.pyplot as plt
# pip install matplotlib pendulum

# ---------------------------------------------------------------------------------------

a = input('Stock 1:')

stock_1 = a

# ---------------------------------------------------------------------------------------

# Stock 1
price_history_1 = yf.Ticker(stock_1).history(period='1y', # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                   interval='1d', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                   actions=False)
print(price_history_1)
time_series1 = list(price_history_1['Close'])
print(time_series1)

# ---------------------------------------------------------------------------------------

time_series1_high = list(price_history_1['High'])
time_series1_low = list(price_history_1['Low'])
range_1 = []
for x in range (0, len(time_series1_high)):
    high = time_series1_high[x]
    low = time_series1_low[x]
    print(high, low)
    range = abs(high - low)
    range_1.append(range)
    print(range)

print(range_1)

atr_14_array = range_1[(len(range_1)-14) : (len(range_1))]

atr = sum(atr_14_array) / 14

print(atr)

# ---------------------------------------------------------------------------------------

# ATR
atr_week = atr * 5
print("one week ATR range: ", atr_week)

one_week_high = time_series1_high[(len(time_series1_high)-5) : (len(time_series1_high))]
print(one_week_high)

one_week_low = time_series1_low[(len(time_series1_low)-5) : (len(time_series1_low))]
print(one_week_low)

one_week_range = abs(max(one_week_high) - min(one_week_low))

print("ATR: ", atr)
print("one week ATR range: ", atr_week)
print("one week current range: ", one_week_range)

# ---------------------------------------------------------------------------------------

# Standard Deviation of ATR
st_dev_of_atr_14_one_day = statistics.stdev(atr_14_array)
print("standard dev range one day: ", st_dev_of_atr_14_one_day)

# Signal, move is greater than 5 days standard dev range. triggers sell signal for covered call / or credit put spread downside
# 68 % of the time it does not exceed this range. so we can sell a covered call into this while premium is rich
st_dev_of_atr_14_one_week = (atr_week*.68)
print("standard dev range one week: ", st_dev_of_atr_14_one_week)

if one_week_range > st_dev_of_atr_14_one_week:
    print("exceeds one standard dev of one week range, consider selling covered call here")

# Update to account for upside alerts for covered calls and downside alters for credit put spreads

# ---------------------------------------------------------------------------------------

# Notes


# what is the standard dev of that weeks data? or the standard dev of that atr 14 day period?

# can also use annualize volatility calculate / 12 IV month then /4 week

# calc what strike to sell

# monitor open positions, when new trade ticker is added to dictionary and runs through measuring open PnL percent. alert >70%

# run backtest with chart showing dot every time covered call signal was triggered

# have program listen and send em ail anytime trigger







# ---------------------------------------------------------------------------------------

# #create DataFrame
# df = pd.DataFrame({stock_1 : time_series1,
#                    stock_2 : time_series2,
#                    'Ratio' : ratio,
#                    'Spread' : spread,
#                    })

# #'Date': date,
# print("average ratio: ", average_ratio)
# print(df)

# df.to_csv('result.csv')

# # ---------------------------------------------------------------------------------------

# # find biggest open loss for each trade
# # pnl graph / equity graph

# # backtest pnl
# trades_pnl = []
# trade_enter = []
# trade_exit = []
# hold_period = []
# open_price = 0
# close_price = 0
# for x in range(0,len(spread)):
#     if spread[x] > st_dev and open_price == 0:
#         open_price = spread[x]
#         trade_enter.append(x)
#         print("trade opened at: ", open_price)
#     elif spread[x] < st_dev*-1 and open_price == 0:
#         open_price = spread[x]
#         trade_enter.append(x)
#         print("trade opened at: ", open_price)
#     if open_price > 1 and spread[x] < 1:
#         close_price = spread[x]
#         trades_pnl.append(open_price - close_price)
#         trade_exit.append(x)
#         hold_period.append(trade_exit[len(trade_exit) - 1] - trade_enter[len(trade_enter) - 1])
#         print("trade closed at: ", close_price)
#         open_price = 0
#         close_price = 0
#     if open_price < -1 and spread[x] > -1:
#         close_price = spread[x]
#         trades_pnl.append(close_price - open_price)
#         trade_exit.append(x)
#         hold_period.append(trade_exit[len(trade_exit) - 1] - trade_enter[len(trade_enter) - 1])
#         print("trade closed at: ", close_price)
#         open_price = 0
#         close_price = 0

# print("trades PnL: ", trades_pnl)
# print("trade enter: ", trade_enter)
# print("trade exit: ", trade_exit)
# print("hold period: ", hold_period)
# print("average hold period: ", sum(hold_period) / len(hold_period) )
# print("number of round trips: ", len(hold_period))
# print("total PnL per unit", sum(trades_pnl))
# print("total profit per 100 shares: $", sum(trades_pnl)*100)


# print("capital used on leg 1:", time_series1[0]*average_ratio*100)
# print("capital used on leg 2:", time_series2[0]*100)
# capital_leg_1 = time_series1[0]*average_ratio*100
# capital_leg_2 = time_series2[0]*100

# total_capital = capital_leg_1 + capital_leg_2
# print("total capital used: ", total_capital)
# total_return = (sum(trades_pnl)*100) / total_capital

# print("r squared: ", R_sq)
# print("standard dev: ", st_dev)
# print("average ratio: ", average_ratio)
# print("total return: ", total_return*100, "%")

# # we want to make it monitor the ratios every minute, not just once a day...

# # csv write line for each loop


# # ---------------------------------------------------------------------------------------

# # Creating a Graph / Chart
# dt_list = [pendulum.parse(str(dt)).float_timestamp for dt in list(price_history_1.index)]
# plt.style.use('dark_background')
# plt.plot(dt_list, spread, linewidth=2)
# plt.axhline(y=st_dev, xmin=0.0, xmax=1.0, color='r')
# plt.axhline(y=0, xmin=0.0, xmax=1.0, color='w')
# plt.axhline(y=(st_dev*-1), xmin=0.0, xmax=1.0, color='r')
# plt.show()