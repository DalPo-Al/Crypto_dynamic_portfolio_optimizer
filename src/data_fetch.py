import yfinance as yf
import pandas as pd

def fetch_crypto_data(ticker, start, end):
  data=yf.download(tickers=ticker, start=start, end=end)["Close"]
  print(data.head())
  #data are automatically imported as dataframe
  data=data.dropna()
  return data

#condition that runs the file only when called directly, we avoid the auto call from importing
#if __name__=="__main__":
#  tickers=["BTC-USD","ETH-USD", "XRP-USD"]
#  data=fetch_crypto_data(start="2022-01-01", end="2025-01-01", ticker=tickers)
#  data.to_csv("data/crypto_data.csv")
#  print("Data saved to data/crypto_data.csv ... :)")


