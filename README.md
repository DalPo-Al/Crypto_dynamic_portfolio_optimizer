### Crypto Portfolio Optimizer
In this project i am interested in estimating the difference in cumulative returns between a dynamic portfolio and a static portfolio based on market regime detection for rebalancing switch. The main question is, using a financial asset that is extremely volatile for definition, what is the best strategy between a static portfolio held for the time period, and   a dynamic portfolio with monthly rebalancing based on signals created from a market regime detection estimator (bullish vs bearish) with transaction cost on turnover of weights?

We use the crypto market to try to handle a financial object that is extremely volatile for definition.

### Optimization engine
For the optimization of the portfolio weights we use the Mean Variance Optimization engine (MVO) that is a convex problem of maximization, that we solve using cvxpy library.

### The market regime detection
In MVO fundamental is the parameter (\lambda)\ i have defined as **risk_penalty** variable. Formally, we estimate the weights according to a different value of risk_penalty according to signal generated from market regime detector.

- **Bullish:** `bullish_penalty = 0.2`  
- **Bearish:** `bearish_penalty = 0.8`  

I recall that **risk_penalty** represents investor risk aversion so:  
- High → prioritize **risk reduction** of portfolio  
- Low → prioritize **return maximization** of portfolio 

### MVO equation used
cp.Maximize(mu @ w - risk_penalty * cp.quad_form(w, sigma))

### Constraints imposed  
- **No short-selling** so weights of portfolio have to be positive => **w>=0**   
- **Fully invested capital** so we ensure the entirety of capital is invested and not held as liquidity => **cp.sum(w)==1**  
- **Limit to single exposure** since i want to ensure diversification in portfolio and avoid the divergence of the problem in allocating all resources into a single asset (that is financially absurd in portfolio management) => **w <= 0.20**  

### Market regime detection system
In order to provide a signal i have defined arbitrarily two market conditions moving average crossover strategy on BTC-USD crypto since i have assumed (by observation of past events) that BTC is the trend maker for the crypto market.
In the specific i have used a Moving average crossover strategy using 200 moving average against 50 moving average.

Formally:
- if MA(50)>MA(200) => GOLDEN CROSS => BULL MARKET => 1
- if MA(50)<=MA(200) => DEATH CROSS => BEAR MARKET => 0

The plot of two curves can be seen in plot/MACS.jpg

### Backtesting
I am interested in defining using in sample testing if the strategy would have been profitable over the time period 2022-2024, so if dynamic portfolio would has been better than a static buy and hold. To do so i have performed a rolling window approach using the window of 1 month (rounghly 30 periods) considering a per unit turnover cost of 0.1% (so 0.001).

The cumulative return can be seen in plot/backtest_comparison.jpg

### Weights computation for last period
Finally i was interested in computing last list of weights for the portfolio and plot them as pie chart, the plot can be seen in plot/asset_allocation.jpg that is valid for last period considered.

### Metrics computation
I have computed Sharpe Ratio and Cumulative last return to compare the strategies and take conclusions.

|Portfolio | Sharpe Ratio | Cumulative Return [%] |
|----------|--------------|-----------------------|
|Dynamic   |         1.240|                  11.51|
|Static    |         0.549|                   1.19|

sharpe computed with risk_free_rate of 0.3% of 1 YEAR US TBILL.


### Conclusions
Based on current information, the Dynamic strategy outperformed the Static one by +10.32%. This performance gap likely reflects the higher volatility of the underlying assets, which the dynamic allocation managed more efficiently. Moreover, the Dynamic Portfolio achieved a Sharpe Ratio higher by +1.240, indicating a superior risk-adjusted return.