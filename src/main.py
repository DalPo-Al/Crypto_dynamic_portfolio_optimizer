from data_fetch import fetch_crypto_data
from optimizer import optimize_portfolio
from backtest import backtest
from market_regime import detect_market_regime
from backtest import performance_stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#PROJECT PARAMETERS
tickers = ["ETH-USD", "SOL-USD", "AVAX-USD", "ADA-USD", "BTC-USD", "XRP-USD"]
start_date="2024-01-01"
end_date="2025-01-01"
window=30 #update portfolio every 30 days
bullish_penalty=0.3
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
  "Cumulative Return[%]":[np.round(dyn["Cumulative Return"]*100, 3), np.round(stat["Cumulative Return"]*100, 3)],
}, index=["Dynamic Strategy", "Static Strategy"])

weights_df =pd.DataFrame({
  "Strategy": ["Dynamic Strategy", "Static Strategy"],
  **{ticker: [dynamic_weights[i], static_weights[i]] for i, ticker in enumerate(prices.columns)}
})
summary=results_df.join(weights_df.set_index("Strategy"))
print("\nPerformance comparison:")
print(summary)
summary.to_csv("data/weights.csv")

#print(results_df)
#print(weights_df)

#RESULT PLOTTING
#cumulative return of portfolios
plt.figure(figsize=(10,6))
plt.plot(result.index, result["Dynamic Strategy"],label="Dynamic Strategy", linewidth=2)
plt.plot(result.index, result["Static Strategy"], label="Static Strategy", linestyle="--")
plt.title("Backtest: Dynamic vs Static Strategy")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.grid(True)
plt.legend()
plt.show()
result.to_csv("data/backtest_results.csv")
print("result saved to data/backtest_results.csv")

#pie chart of final weights for the month
plt.figure(figsize=(10,6))
labels=[f"{t}({w:.2f}%)" for t,w in zip(tickers, dynamic_weights)]   
plt.pie(dynamic_weights, labels=labels)
plt.title("Weights allocation of the month")
plt.show()