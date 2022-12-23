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

import schedule
import time
import csv
from email.message import EmailMessage 
import ssl
import smtplib

import os
from dotenv import load_dotenv
load_dotenv()
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# ---------------------------------------------------------------------------------------

alert_list = []
results = []

# ---------------------------------------------------------------------------------------

# stock_list = ['AMZN', 'GOOG', 'TSLA', 'NVDA', 'NFLX', 'PYPL', 'META', 'SHOP', 'SQ', 'CRWD', 'ETHE', 'UPST', 'CAT', 'HD', 'LRCX', 'AMD', 'ABNB', 'ADBE', 'CRM', 'ROKU', 'SE', 'DDOG', 'NET'] # , 'MGK', 'QYLD'
# stock_list = ['UNH', 'SYK', 'DE', 'HD', 'CNHI', 'CVS', 'NEE', 'AME', 'SANM', 'CSX', 'NKE', 'SBUX', 'FSLR', 'NFLX', 'CTVA', 'CSCO', 'MBLY', 'ED', 'GM', 'AMD', 'ALGM', 'FTNT', 'PYPL', 'NVDA']

# combined
stock_list = ['AMZN', 'GOOG', 'TSLA', 'NVDA', 'NFLX', 'PYPL', 'META', 'SHOP', 'SQ', 'CRWD', 'ETHE', 'UPST', 'CAT', 'HD', 'LRCX', 'AMD', 'ABNB', 'ADBE', 'CRM', 'ROKU', 'SE', 'DDOG', 'NET', 'UNH', 'SYK', 'DE', 'HD', 'CNHI', 'CVS', 'NEE', 'AME', 'SANM', 'CSX', 'NKE', 'SBUX', 'FSLR', 'CTVA', 'CSCO', 'MBLY', 'ED', 'GM', 'AMD', 'ALGM', 'FTNT', 'PYPL'] # , 'MGK', 'QYLD'

# ---------------------------------------------------------------------------------------
def atr_scan():
    for x in range(0,len(stock_list)):
        stock = stock_list[x]
        price_history = yf.Ticker(stock_list[x]).history(period='1y', # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                        interval='1d', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                        actions=False)
        print(price_history)
        
        series_close = list(price_history['Close'])
        series_high = list(price_history['High'])
        series_low = list(price_history['Low'])
        # print(series_close)
        # print(series_high)
        # print(series_low)

    # ---------------------------------------------------------------------------------------

        stock_range = []
        for x in range(0,len(series_high)):
            high = series_high[x]
            low = series_low[x]
            print(high, low)
            x_range = abs(high - low)
            stock_range.append(x_range)
            print(stock_range)

        print(stock_range)

    # ---------------------------------------------------------------------------------------

        # ATR
        atr_14_array = stock_range[(len(stock_range)-14) : (len(stock_range))]

        atr = sum(atr_14_array) / 14

        print(atr)

    # ---------------------------------------------------------------------------------------

        # Benchmarks
        atr_week = atr * 5
        print("one week ATR range: ", atr_week)

        one_week_high = series_high[(len(series_high)-5) : (len(series_high))]
        print(one_week_high)

        one_week_low = series_low[(len(series_low)-5) : (len(series_low))]
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

        data = {'stock':stock, 
                'atr':atr, 
                'atr_week':atr_week, 
                'one_week_high':max(one_week_high), 
                'one_week_low':min(one_week_low), 
                'st_dev_of_atr_14_one_week':st_dev_of_atr_14_one_week, 
                'one_week_range':one_week_range
                }

        if one_week_range > st_dev_of_atr_14_one_week:
            print(f" {stock}: {one_week_range} exceeds one standard dev of one week range {st_dev_of_atr_14_one_week}")
            stock_name = data['stock']
            if stock_name not in alert_list:
                alert_list.append(stock_name)
                results.append(data)
                send_email(data, stock_name)
            # else:
            #     results.remove(data)
            #     results.append(data)
        
        # elif one_week_range <= st_dev_of_atr_14_one_week:
        #     if data in results:
        #         alert_list.remove(stock_name)
        #         results.remove(data)


            # df = df.append(data, ignore_index=True)
            # if , send email 

        # Update to account for upside alerts for covered calls and downside alters for credit put spreads

    # ---------------------------------------------------------------------------------------

    print(results)

    df = pd.DataFrame(results)

    print(df)

    df.to_csv('atr_signals.csv')

    # print(time.now())
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)

#------------------------------------------------------------------------------------------------

def send_email(data, stock_name):
    email_sender = 'joshua.becker91@gmail.com'
    email_password = EMAIL_PASSWORD
    email_receiver = 'joshua.becker91@gmail.com' # can enter an array with multiple email receivers

    subject = f'New ATR move alert on {stock_name}'

    body = f'''
{data['stock']} has made > 5 day standard dev move

Stock: {data['stock']} 

ATR: {round(data['atr'], 2)} 

ATR Week: {round(data['atr_week'], 2)} 

Sandard Dev of One Week: {round(data['st_dev_of_atr_14_one_week'], 2)}  

Current one week range: {round(data['one_week_range'], 2)} 
    '''

    # html=f'<h1>BTC is trading at {last_quote}</h1>' can also have html code here to customize styling/embeds/links

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("email successfully sent")
    except:
        print("error sending email")

#------------------------------------------------------------------------------------------------

# def clear_results():
    # results = []

# schedule.every(5).days.do(clear_results)

schedule.every(5).minutes.do(atr_scan)

while True:
    schedule.run_pending()
    time.sleep(1)

#------------------------------------------------------------------------------------------------

# Consider making the alerts specify if it has reached the ATR move on a move up or move down













#create DataFrame
# df = pd.DataFrame({'stock':stock, 
#                     'atr':atr, 
#                     'atr_week':atr_week, 
#                     'one_week_high':one_week_high, 
#                     'one_week_low':one_week_low, 
#                     'st_dev_of_atr_14_one_week':st_dev_of_atr_14_one_week, 
#                     'one_week_range':one_week_range
#                     })


# fieldnames = ['stock','atr','atr_week','one_week_high','one_week_low','st_dev_of_atr_14_one_week','one_week_range']
# thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
# thewriter.writeheader()
# for item in data:
    # thewriter.writerow(item)
# with open('atr_signals.csv', 'a', newline='') as csvfile:
        #     data = {'stock':stock, 
        #             'atr':atr, 
        #             'atr_week':atr_week, 
        #             'one_week_high':one_week_high, 
        #             'one_week_low':one_week_low, 
        #             'st_dev_of_atr_14_one_week':st_dev_of_atr_14_one_week, 
        #             'one_week_range':one_week_range
        #     }


# Notes


# what is the standard dev of that weeks data? or the standard dev of that atr 14 day period?

# can also use annualize volatility calculate / 12 IV month then /4 week

# calc what strike to sell

# monitor open positions, when new trade ticker is added to dictionary and runs through measuring open PnL percent. alert >70%

# run backtest with chart showing dot every time covered call signal was triggered

# have program listen and send em ail anytime trigger



# ---------------------------------------------------------------------------------------

# #create DataFrame
# df = pd.DataFrame({stock_1 : series,
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


# print("capital used on leg 1:", series[0]*average_ratio*100)
# print("capital used on leg 2:", time_series2[0]*100)
# capital_leg_1 = series[0]*average_ratio*100
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
# dt_list = [pendulum.parse(str(dt)).float_timestamp for dt in list(price_history.index)]
# plt.style.use('dark_background')
# plt.plot(dt_list, spread, linewidth=2)
# plt.axhline(y=st_dev, xmin=0.0, xmax=1.0, color='r')
# plt.axhline(y=0, xmin=0.0, xmax=1.0, color='w')
# plt.axhline(y=(st_dev*-1), xmin=0.0, xmax=1.0, color='r')
# plt.show()