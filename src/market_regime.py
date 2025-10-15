#Define market regime 
#Moving average crossover strategy

import pandas as pd #to use rolling function
import matplotlib.pyplot as plt

def plotting(short_ma, long_ma, prices):
  plt.figure(figsize=(12,6))
  plt.plot(short_ma, color="blue", label="50_MA")
  plt.plot(long_ma, color="red", label="200_MA")
  plt.plot(prices, color="black", label="BTC_price")
  plt.title("Moving Average CrossOver")
  plt.legend()
  plt.grid(True, color="grey")
  plt.savefig("plot/MACS.jpg")
  plt.show()

def detect_market_regime(prices, short_window=50, long_window=200):
  #compute 50MA 
  short_ma=prices.rolling(window=short_window).mean() #single value
  #compute 200MA
  long_ma=prices.rolling(window=long_window).mean() #single value
  #condition implementation for bullish market regime
  regime=(short_ma>long_ma).astype(int) #since we want 1 if True and 0 if False
  plotting(short_ma=short_ma, long_ma=long_ma, prices=prices)
  return regime

if __name__=="__main__":
  prices=pd.read_csv("data/crypto_data.csv", parse_dates=True, index_col=0)
  regime=detect_market_regime(prices)
  print("Market Regime (1: Bullish, 0: Bearish):")
  print(regime.tail())