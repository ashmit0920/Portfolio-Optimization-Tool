# Portfolio-Optimization-Tool

A portfolio optimization tool helps investors allocate their assets in a way that maximizes return for a given level of risk or minimizes risk for a given level of return. One common approach is using the Modern Portfolio Theory (MPT), developed by Harry Markowitz, which focuses on the trade-off between risk and return.

## Install Required Libraries

```
pip install pandas numpy matplotlib scipy yfinance cvxpy
```

## Working 

The expected returns and covariance matrix is calculated for 5 companies. An optimization function is defined to maximize the Sharpe ratio. Certain constraints are added to ensure a more balanced portfolio and avoid "corner solutions", such as setting minimum and maximum weights for each asset. Another approach is to add a regularization term to the optimization objective to penalize highly concentrated portfolios. At the end, the efficient frontier is plotted for visualization purposes.