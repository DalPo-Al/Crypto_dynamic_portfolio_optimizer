# Crypto Portfolio Optimizer

## Description
Dynamic **crypto portfolio optimizer** with **monthly rebalancing**, transaction costs (0.1%), and **market regime detection** (bullish vs bearish).  

The optimizer adjusts the **risk penalty** parameter (\(\lambda\)) according to market regime:  

- **Bullish:** `bullish_penalty = 0.3`  
- **Bearish:** `bearish_penalty = 0.8`  

Where **risk_penalty** represents investor risk aversion:  
- High → prioritize **risk reduction**  
- Low → prioritize **return maximization**  

The optimizer solves a **convex optimization problem** using `cvxpy`:

cp.Maximize(mu @ w - risk_penalty * cp.quad_form(w, sigma))

**Constraints:**  
- No short-selling: w>=0  
- Fully invested: cp.sum(w)==1  
- Max weight per asset: w <= 0.25  

Performance is benchmarked against a **Buy & Hold strategy** with a static initial portfolio.

---

## Features
- Fetch historical crypto prices via **Yahoo Finance API**.  
- Optimize portfolio allocation using **convex optimization** (`cvxpy`) with risk penalty.  
- Detect **market regimes** using moving average crossover (50-day vs 200-day).  
- Apply **rebalancing costs** proportional to portfolio turnover.  
- Compare dynamic rebalancing vs Buy & Hold in a **backtesting framework**.  
- Calculate key **performance metrics**: cumulative return, volatility, Sharpe ratio.  
- Save results as **CSV** for further analysis.  
- Plot **cumulative returns** over time.  
- Plot **final optimal portfolio weights** as a pie chart.

---

## File Structure
crypto-portfolio-optimizer/
│
├─ src/
│ ├─ main.py                # Integrates all modules and runs backtest
│ ├─ optimizer.py           # Portfolio optimization logic
│ ├─ data_fetch.py          # Fetch historical crypto data
│ ├─ market_regime.py       # Market regime detection
│ └─ backtest.py            # Rolling-window backtesting framework
│
├─ data/
│ ├─ crypto_data.csv        # Historical price data
│ └─ backtest_results.csv   # Backtest output
│
├─ README.md
└─ requirements.txt
