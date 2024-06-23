# Portfolio-Optimization-Tool

A portfolio optimization tool helps investors allocate their assets in a way that maximizes return for a given level of risk or minimizes risk for a given level of return. One common approach is using the Modern Portfolio Theory (MPT), developed by Harry Markowitz, which focuses on the trade-off between risk and return.

## Install Required Libraries

Type the following command in your terminal.
```
pip install pandas numpy matplotlib scipy yfinance cvxpy
```

## Working 

The expected returns and covariance matrix is calculated for 5 companies. An optimization function is defined to maximize the Sharpe ratio. Certain constraints are added to ensure a more balanced portfolio and avoid "corner solutions", such as setting minimum and maximum weights for each asset. Another approach is to add a regularization term to the optimization objective to penalize highly concentrated portfolios. At the end, the efficient frontier is plotted for visualization purposes.

## Future updates

- **Enhance the Model:** Incorporate more sophisticated risk measures, such as Value at Risk (VaR) or Conditional Value at Risk (CVaR).

- **User Interface:** Building a web interface using Flask or Dash to allow users to input their own preferences and view results dynamically.

- **Performance Monitoring:** Set up a system to track the performance of the optimized portfolio over time and compare it with benchmarks.