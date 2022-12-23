"# covered_call_signal_pandas_yfinance" 

Stock screener runs throughout the day in real time and send email notifications when criteria has been met for a stock on your watchlist. This identifies options premiums that have become rich by signaling when the stock has made a 5 day standard deviation move based on ATR for that stock. This signal alerts the opportunity to sell a covered call (or close one for profit) when the premium has become rich therefore contributing alpha to the portfolio. Pandas dataframe is utilized to capture data retrieved from yfinance and saved to csv and emailed to you automatically.

Technologies used: Python, Pandas, numpy, smtplib, schedule, yfinance, csv

Currently in development...

![image](https://user-images.githubusercontent.com/98496684/209392766-c232ef04-661a-4309-af72-3f1e72782cb0.png)
