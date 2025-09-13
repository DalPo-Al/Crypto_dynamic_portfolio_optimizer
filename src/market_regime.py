#Define market regime 
#Moving average crossover strategy
#if price>200MA => bullish else bearish

import pandas as pd #to use rolling function

def detect_market_regime(prices, short_window=50, long_window=200):
  #compute 50MA 
  short_ma=prices.rolling(window=short_window).mean() #single value
  #compute 200MA
  long_ma=prices.rolling(window=long_window).mean() #single value

  #condition implementation for bullish market regime
  regime=(short_ma>long_ma).astype(int) #since we want 1 if True and 0 if False
  
  return regime

#if __name__=="__main__":
#  prices=pd.read_csv("data/crypto_data.csv", parse_dates=True, index_col=0)
#  regime=detect_market_regime(prices)
#  print("Market Regime (1: Bullish, 0: Bearish):")
#  print(regime.tail())