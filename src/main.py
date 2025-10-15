from data_fetch import fetch_crypto_data
from optimizer import optimize_portfolio
from backtest import backtest
from market_regime import detect_market_regime
from backtest import performance_stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#PROJECT PARAMETERS
tickers = ["BTC-USD", "ETH-USD", "SOL-USD", "AVAX-USD", "ADA-USD", "XRP-USD", "LINK-USD"]
start_date="2022-01-01"
end_date="2025-01-01"
window=30 #update portfolio every 30 days
bullish_penalty=0.2
bearish_penalty=0.8
risk_penalty=0.5

#DATA FETCHING
prices=fetch_crypto_data(tickers, start=start_date, end=end_date)
prices.to_csv("data/crypto_data.csv")
print("Data saved to data/crypto_data.csv ... :)")

#OPTIMIZATION
result=optimize_portfolio(prices, risk_penalty)

#DETECT MARKET REGIME
regime=detect_market_regime(prices["BTC-USD"])

#BACKTEST
print("\nDynamic portfolio vs Static portfolio strategy)")
result, dynamic_portfolio_return, static_portfolio_return,static_weights, dynamic_weights=backtest(prices, window, bullish_penalty, bearish_penalty)

print(f"static_weights: {static_weights}")
print(f"dynamic_weights: {dynamic_weights}")

#COMPARISON
dyn=performance_stats(dynamic_portfolio_return)
stat=performance_stats(static_portfolio_return)

results_df=pd.DataFrame({
  "Sharpe Ratio": [np.round(dyn["Sharpe Ratio"], 3),np.round(stat["Sharpe Ratio"],3)],
  "Cumulative Return[%]":[np.round(((1+dynamic_portfolio_return).cumprod()-1)*100, 3), np.round(((1+static_portfolio_return).cumprod()-1)*100, 3)],
}, index=["Dynamic Strategy", "Static Strategy"])

weights_df =pd.DataFrame({
  "Strategy": ["Dynamic Strategy", "Static Strategy"],
  **{ticker: [dynamic_weights[i], static_weights[i]] for i, ticker in enumerate(prices.columns)}
})
summary=results_df.join(weights_df.set_index("Strategy"))
print("\nPerformance comparison:")
print(summary)
summary.to_csv("data/weights.csv")



dyn_ret=np.round(((1+dynamic_portfolio_return).cumprod()-1).iloc[-1], 2)
stat_ret=np.round(((1+static_portfolio_return).cumprod()-1).iloc[-1], 2)

print(f"Static portfolio cumulative return: {stat_ret} %")
print(f"Dynamic portfolio cumulative return: {dyn_ret} %")
print(f"Dynamic outperformed Static of: {(dyn_ret)-(stat_ret)}%")

#RESULT SAVING
result.to_csv("data/backtest_results.csv")
print("result saved to data/backtest_results.csv")

#RESULT PLOTTING
#cumulative return of portfolios
dynamic_portfolio_return=np.round(((1+dynamic_portfolio_return).cumprod()-1), 2)
static_portfolio_return=np.round(((1+static_portfolio_return).cumprod()-1), 2)
plt.figure(figsize=(10,6))
plt.plot(dynamic_portfolio_return.index, dynamic_portfolio_return, label="Dynamic Strategy", linewidth=2)
plt.plot(static_portfolio_return.index, static_portfolio_return, label="Static Strategy", linestyle="--")
plt.title("Backtest: Dynamic vs Static Strategy - Cumulative Return")
plt.ylabel("Cumulative return [%]")
plt.legend()
plt.grid(True)
plt.savefig("plot/backtest_comparison.png", dpi=300, bbox_inches="tight")
plt.show()

#pie chart of final weights for the month
plt.figure(figsize=(10,6))
labels=[f"{t}({w:.2f}%)" for t,w in zip(tickers, dynamic_weights)]   
plt.pie(dynamic_weights, labels=labels)
plt.title("Portfolio allocation (last, dynamic)")
plt.savefig("plot/asset_allocation.png", dpi=300, bbox_inches="tight")
plt.show()