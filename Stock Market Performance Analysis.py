# -------------------------------------------------------------------------------------------------------------------
# -- Stock Market Performance Analysis involves calculating moving averages, measuring volatility, 
# conducting correlation analysis and analyzing various aspects of the stock market to gain a deeper understanding of
# the factors that affect stock prices and the relationships between the stock prices of different companies. --
# --------------------------------------------------------------------------------------------------------------------

# Import Libraries

import pandas as pd
import yfinance as yf
import numpy as np

# Import datetime module
from datetime import datetime

# Download the historical stock price data for four companies: Apple, Microsoft, Netflix, and Google, for the last three months.

start_date = datetime.now() - pd.DateOffset(months=3)
end_date = datetime.now()

tickers = ['AAPL', 'MSFT', 'NFLX', 'GOOG']

df_list = []      # is a list containing multiple pandas DataFrames that I want to concatenate.

for ticker in tickers:
    data = yf.download(ticker,start= start_date,end= end_date)
    df_list.append(data)

df = pd.concat(df_list, keys=tickers, names=['Ticker', 'Date']) # This code concatenates a list of DataFrames into a single DataFrame,
print(df.head())

df = df.reset_index()                                           # It is used to reset the index to the default integer index.
print(df.head())

# Let’s have a look at the performance in the stock market of all the companies:

import plotly.express as px

fig = px.line(df, x= "Date",
              y="Close",
              color="Ticker",
              title="Stock Market Performance for the Last 3 Months")

fig.show()

print("=" * 70)

# The faceted area chart, which makes it easy to compare the performance of different companies and identify similarities or differences in their stock price movements.

fig = px.area(df,x="Date",y="Close",color="Ticker",facet_col="Ticker",
              labels={"Date": "Date", "Close" : "Closing Price", "Ticker" : "Company"}, 
              title= "Stock Prices for Apple, Microsoft, Netflix and Google ")
fig.show()

print("=" * 70)

# -- Analyzing Moving Averages --
# -- It Provides a useful way to identify trends and patterns in each company’s stock price movements over a period of time.

df["MA10"] = (df.groupby("Ticker")['Close'].rolling(window= 10)).mean().reset_index(0, drop = True)
df["MA20"] = (df.groupby("Ticker")['Close'].rolling(window= 20)).mean().reset_index(0, drop = True)

for ticker, group in df.groupby('Ticker'):
    print(f"Moving Averages for {ticker}")
    print(group[['MA10' , 'MA20']])

print("=" * 70)

# -- Visualize the Moving Averages of all Companies -- 

for ticker, group in df.groupby('Ticker'):
    fig = px.line(group, x= "Date",
              y=["Close","MA10","MA20"],
              title=(f"{ticker} Moving Averages"))

    fig.show()

# -- NOTE --
# When the MA10 crosses above the MA20, it is considered a bullish signal indicating that the stock price will continue to rise,
# Conversely, when the MA10 crosses below the MA20, it is a bearish signal that the stock price will continue falling.

print("=" * 70)

# -- Analyze the Volatility --
# -- Volatility is a measure of how much and how often the stock price or market fluctuates over a given period of time --

df["Volatility"] = df.groupby("Ticker")["Close"].pct_change().rolling(window=10).std().reset_index(0,drop=True)     

# Percentage Change: pct_change() is used to get percentage change between the current and a prior element. 

fig = px.line(df,x="Date",y="Volatility",
              color="Ticker",
              title="Volatility of All Companies")
fig.show()

#  -- NOTE --
# High volatility indicates that the stock or market experiences large and frequent price movements, 
# While low volatility indicates that the market experiences smaller or less frequent price movements.

print("=" * 70)

# -- Analyze the correlation between the stock prices of Apple and Microsoft --

# First: Create a DataFrame with the stock prices of Apple and Microsoft:

apple = df.loc[df["Ticker"]=="AAPL",["Date","Close"]].rename(columns={"Close" : "AAPL"})
microsoft = df.loc[df["Ticker"]=="MSFT",["Date","Close"]].rename(columns={"Close" : "MSFT"})
df_corr = pd.merge(apple,microsoft,on="Date")

fig = px.scatter(df_corr,x="AAPL",y="MSFT",
                 trendline="ols",
                 title="The Correlation between Apple and Microsoft")
fig.show()

# There is a strong linear relationship between the stock prices of Apple and Microsoft, 
# which means that when the stock price of Apple increases, the stock price of Microsoft also tends to increase. 
# It is a sign of a strong correlation or similarity between the two companies.

print("=" * 70)

# -- Analyze the correlation between the stock prices of Netflix and Google --

# First: Create a DataFrame with the stock prices of Netflix and Google:

netflix = df.loc[df["Ticker"]=="NFLX",["Date","Close"]].rename(columns={"Close" : "NFLX"})
google = df.loc[df["Ticker"]=="GOOG",["Date","Close"]].rename(columns={"Close" : "GOOG"})
df_corr = pd.merge(netflix,google,on="Date")

fig = px.scatter(df_corr,x="NFLX",y="GOOG",
                 trendline="ols",
                 title="The Correlation between Netflix and Google")
fig.show()

# It is a sign of a weak correlation between the two companies.

print("=" * 70)

# -- Analyze the correlation between the stock prices of Netflix and Apple --

df_corr = pd.merge(netflix,apple,on="Date")
fig = px.scatter(df_corr,x="NFLX",y="AAPL",
                 trendline="ols",
                 title="The Correlation between Netflix and Apple")
fig.show()

# There is a strong linear relationship between the stock prices of Netflix and Apple.

print("=" * 70)

# -- Analyze the correlation between the stock prices of Google and Microsoft --

df_corr = pd.merge(google,microsoft,on="Date")
fig = px.scatter(df_corr,x="GOOG",y="MSFT",
                 trendline="ols",
                 title="The Correlation between Google and Microsoft")
fig.show()