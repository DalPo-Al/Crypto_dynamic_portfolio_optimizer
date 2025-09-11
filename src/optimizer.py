#optimization engine of the project
#optimization logic: SHARPE RATIO MAXIMIZATION

import pandas as pd
import numpy as np
import cvxpy as cp #engine

def optimize_portfolio(prices, risk_penalty):
  #risk penalty controls risk adversion
  #high risk penalty -> focus on reducing the risk
  #low risk penalty => focu on maximizing the return

  #consecutive return
  returns=prices.pct_change().dropna() #(1095, 3)
  #average return per asset
  mu=returns.mean().values #(3,)
  #covariance matrix for returns
  sigma=returns.cov().values #(3, 3)
  #variable of optimization
  n=len(mu)
  w=cp.Variable(n)
  
  # objective function
  obj = cp.Maximize(mu @ w - risk_penalty * cp.quad_form(w, sigma))
  
  # constraints
  constraints=[w>=0, cp.sum(w)==1]
  cp.Problem(obj, constraints).solve()
  weights=np.array(w.value).flatten() #(3,)
  
  portfolio_return=mu@weights #(scalar)
  portfolio_volatility=np.sqrt(weights@sigma@weights) #(scalar)
  portfolio_sharpe=portfolio_return/portfolio_volatility if portfolio_volatility>0 else 0 #(scalar)

  results={
    "optimal_weights":pd.Series(weights, index=prices.columns),
    "expected_return_portfolio":portfolio_return,
    "portfolio_volatility":portfolio_volatility,
    "portfolio_sharpe":portfolio_sharpe
  }
  return results

if __name__=="__main__":
  prices=pd.read_csv("data/crypto_data.csv", index_col=0, parse_dates=True)
  result=optimize_portfolio(prices, risk_penalty=0.5)
  print("Optimized portfolio weights:")
  print(result["optimal_weights"])
  print(f"Expected return: {result['expected_return_portfolio']:.4f}")
  print(f"Volatility: {result['portfolio_volatility']:.4f}")
  print(f"Sharpe ratio: {result['portfolio_sharpe']:.4f}")