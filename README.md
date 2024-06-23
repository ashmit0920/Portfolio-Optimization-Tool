# Portfolio-Optimization-Tool

A portfolio optimization tool helps investors allocate their assets in a way that maximizes return for a given level of risk or minimizes risk for a given level of return. One common approach is using the Modern Portfolio Theory (MPT), developed by Harry Markowitz, which focuses on the trade-off between risk and return.

## Install Required Libraries

Setup a virtual environment to prevent dependency conflicts (highly recommended). Type the following commands in a Windows terminal inside the project directory.
```
python -m venv venv
```
```
venv\Scripts\Activate
```
Install the required libraries.
```
pip install dash dash-bootstrap-components yfinance pandas numpy matplotlib scipy cvxpy
```

## Working 

The expected returns and covariance matrix is calculated for 5 companies, the yfinance library is used to collect the data. An optimization function is defined to maximize the Sharpe ratio. Certain constraints are added to ensure a more balanced portfolio and avoid "corner solutions", such as setting minimum and maximum weights for each asset. Another approach is to add a regularization term to the optimization objective to penalize highly concentrated portfolios. At the end, the efficient frontier is plotted for visualization purposes.

The user interface is created using **Dash**, a web framework for building analytical web applications in Python. The UI provides input fields to enter the company names (ticker symbols), start and end dates for the data to be analyzed and a Risk Tolerance slider.

On clicking the "Optimize" button, a Return v/s Volatility graph is plotted and the Optimal weights and various other performance metrics are calculated and displayed. The "X" in the graph symbolizes the maximum **Sharpe Ratio**.

![UI screenshot](./User%20Interface.png)

## Future updates

- **Enhance the Model:** Incorporate more sophisticated risk measures, such as Value at Risk (VaR) or Conditional Value at Risk (CVaR).

- **User Interface:** Building a web interface using Flask or Dash to allow users to input their own preferences and view results dynamically.

- **Performance Monitoring:** Set up a system to track the performance of the optimized portfolio over time and compare it with benchmarks.