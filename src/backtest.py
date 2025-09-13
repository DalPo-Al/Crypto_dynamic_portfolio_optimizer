#backtest of the strategy comparing dynamic optimized portfolio with static strategy
import pandas as pd
import numpy as np
from optimizer import optimize_portfolio
from market_regime import detect_market_regime
import matplotlib.pyplot as plt
  
def backtest(prices,window, bullish_penalty, bearish_penalty, transaction_cost=0.1):
  asset_returns=prices.pct_change().dropna() #(1095, 3)
  
  #DYNAMIC STRATEGY
  market_regime=detect_market_regime(prices["BTC-USD"])
  portfolio_overall_returns=[]
  portfolio_overall_index=[]
  prev_weights=None

  for start in range(0, len(prices)-window, window):
    end=start+window
    prices_iteration=prices.iloc[start:end]
    regime_iteration=market_regime.iloc[end] #we take last day only
    penalty=bullish_penalty if regime_iteration==1 else bearish_penalty

    optimization_result=optimize_portfolio(prices_iteration, risk_penalty=penalty)
    weights=optimization_result["optimal_weights"].values #(3,)
    weights=np.round(weights,2) #ROUND
    #compute daily return
    if (end-start)<=window:
      daily_returns=asset_returns.iloc[start:end] @ weights
    else:
      daily_returns=asset_returns.iloc[start:] @ weights


    ###If we rebalanced and the new portfolio is different from the old one, 
    # then calculate how much trading was done (turnover), 
    # multiply by the fee, and subtract that cost from the portfolio’s return 
    # for the last return available in the vector.
    ###
    #transaction cost at rebalance
    if prev_weights is not None and not (prev_weights==weights).all():
      turnover=np.abs(weights-prev_weights).sum()
      cost=transaction_cost*turnover
      daily_returns.iloc[-1]-=cost #apply the cost to last element of the return vector
      
    portfolio_overall_returns.extend(daily_returns.tolist()) #values
    portfolio_overall_index.extend(daily_returns.index) #indexes
  
  dynamic_portfolio_return = pd.Series(portfolio_overall_returns, index=portfolio_overall_index)
  
  #STATIC STRATEGY
  optimization_result_static=optimize_portfolio(prices,risk_penalty=0.5)
  weights_static=optimization_result_static["optimal_weights"].values #(3,)
  weights_static=np.round(weights_static,2) #ROUND
  daily_returns_static=asset_returns @ weights_static
  
  backtest_result={
    "Dynamic Strategy": dynamic_portfolio_return.cumsum(), #cumulative return
    "Static Strategy": daily_returns_static.loc[dynamic_portfolio_return.index].cumsum()
  }

  result=pd.DataFrame(backtest_result)
  return result, dynamic_portfolio_return, daily_returns_static.loc[dynamic_portfolio_return.index], weights_static, weights

def performance_stats(strategy_returns):
  expected_return=strategy_returns.mean()
  standard_deviation_return=strategy_returns.std()
  sharpe_ratio=expected_return/standard_deviation_return * np.sqrt(252) if standard_deviation_return>0 else 0 #annualized sharpe ratio
  cumulative_return=(1+strategy_returns).prod()-1 #known formula

  stats={
    "Cumulative Return": cumulative_return,
    "Investment Risk (Std Dev)": standard_deviation_return * np.sqrt(252), #annualized std dev
    "Sharpe Ratio": sharpe_ratio,  }

  return stats

#if __name__=="__main__":
#  prices=pd.read_csv("data/crypto_data.csv", index_col=0, parse_dates=True)
#  result, dynamic_portfolio_return, static_portfolio_return, static_weights, dynamic_weights=backtest(
#    prices, 90, 0.2, 1.0)
#  
#  print(static_weights)
#  print(dynamic_weights)
#
#  performance_stats(dynamic_portfolio_return)
#  performance_stats(static_portfolio_return)
#
#  plt.figure(figsize=(10,6))
#  plt.plot(result.index, result["Dynamic Strategy"],label="Dynamic Strategy", linewidth=2)
#  plt.plot(result.index, result["Static Strategy"], label="Static Strategy", linestyle="--")
#  plt.title("Backtest: Dynamic vs Static Strategy")
#  plt.xlabel("Date")
#  plt.ylabel("Cumulative Return")
#  plt.grid(True)
#  plt.legend()
#  plt.show()
#
#  result.to_csv("data/backtest_results.csv")
#  print("result saved to data/backtest_results.csv")